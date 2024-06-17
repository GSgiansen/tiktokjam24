import os
from typing import Optional, List

from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

from bson import ObjectId
import motor.motor_asyncio
from pymongo import MongoClient, ReturnDocument
from dotenv import load_dotenv

from fastapi import FastAPI, File, UploadFile
from io import StringIO
import csv

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from dotenv import dotenv_values

app = FastAPI(
    title="TechJamAPI",
    summary="Backend API for the TechJam project",
)


config = dotenv_values(".env")
# client = MongoClient(os.environ["MONGODB_URL"])
# print(os.environ["MONGODB_URL"])
# db = client["MyDB"]
# csv_collection = db.techjam

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

@app.on_event("startup")
async def startup_event():
    app.mongodb_client = MongoClient(config["MONGODB_URL"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    app.csv_collection = app.database[config["COLLECTION_NAME"]]

    print("Connected to the MongoDB database!")
@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

class CSVModel(BaseModel):
    """
    Container for a single csv record.
    """

    # The primary key for the csvModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    data: List[dict] = Field(default_factory=list)


# class UpdateCSVModel(BaseModel):
#     """
#     A set of optional updates to be made to a document in the database.
#     """


class CSVCollection(BaseModel):
    """
    A container holding a list of `csvModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    csvs: List[CSVModel]


@app.post(
    "/csvs/",
    response_description="Add new csv File",
    response_model=CSVModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_csv(file: UploadFile = File(...)):
    """
    Insert a new csv record.

    A unique `id` will be created and provided in the response.
    """
    data = []

    # Read file as bytes and decode bytes into text stream
    file_bytes = file.file.read()
    buffer = StringIO(file_bytes.decode('utf-8'))

    # Process CSV
    csv_reader = csv.DictReader(buffer)
    for row in csv_reader:
        data.append(row)

    # Close buffer and file
    buffer.close()
    file.file.close()

    csv_record = CSVModel(data=data)

    new_csv =  app.csv_collection.insert_one(
        csv_record.model_dump(by_alias=True, exclude=["id"])
    )
    created_csv = app.csv_collection.find_one(
        {"_id": new_csv.inserted_id}
    )

    return created_csv

@app.get(
    "/csvs/",
    response_description="List all csv files",
    response_model=CSVCollection,
    response_model_by_alias=False,
)
async def list_csvs():
    """
    List all of the csv data in the database.

    The response is unpaginated and limited to 1000 results.
    """
    return CSVCollection(csvs=await app.csv_collection.find().to_list(1000))


@app.get(
    "/csvs/{id}",
    response_description="Get a single csv",
    response_model=CSVModel,
    response_model_by_alias=False,
)
async def show_csv(id: str):
    """
    Get the record for a specific csv, looked up by `id`.
    """
    if (
        csv := await csv_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return csv

    raise HTTPException(status_code=404, detail=f"csv {id} not found")


# @app.put(
#     "/csvs/{id}",
#     response_description="Update a csv",
#     response_model=CSVModel,
#     response_model_by_alias=False,
# )
# async def update_csv(id: str, csv: UpdateCSVModel = Body(...)):
#     """
#     Update individual fields of an existing csv record.

#     Only the provided fields will be updated.
#     Any missing or `null` fields will be ignored.
#     """
#     csv = {
#         k: v for k, v in csv.model_dump(by_alias=True).items() if v is not None
#     }

#     if len(csv) >= 1:
#         update_result = await csv_collection.find_one_and_update(
#             {"_id": ObjectId(id)},
#             {"$set": csv},
#             return_document=ReturnDocument.AFTER,
#         )
#         if update_result is not None:
#             return update_result
#         else:
#             raise HTTPException(status_code=404, detail=f"csv {id} not found")

#     # The update is empty, but we should still return the matching document:
#     if (existing_csv := await csv_collection.find_one({"_id": id})) is not None:
#         return existing_csv

#     raise HTTPException(status_code=404, detail=f"csv {id} not found")


@app.delete("/csvs/{id}", response_description="Delete a csv")
async def delete_csv(id: str):
    """
    Remove a single csv record from the database.
    """
    delete_result = await app.csv_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"csv {id} not found")
