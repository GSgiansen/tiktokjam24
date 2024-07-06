from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os
import json
import csv
import chardet
import pandas as pd
from dotenv import load_dotenv
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import create_model
from backend.db import get_supabase_client

supabase = get_supabase_client()
load_dotenv()

MAX_ROWS = 75

def retrieve_and_augment_data(**context):
    filepath = context['dag_run'].conf.get('filepath')
    dirpath = context['dag_run'].conf.get('dirpath')
    iter_count = context['dag_run'].conf.get('iter_count')
    input = context['dag_run'].conf.get('input')



    response = supabase.storage.from_("synthesize_data").download(path=f"{filepath}")

    split = filepath.split("/")
    if not os.path.exists(split[0]):
        print("split[0] ", split[0])
        os.makedirs(split[0])
    

    print("file_path", filepath)

    with open(filepath, "wb") as file:
            file.write(response)

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.9)
    model = embed_data(filepath, dirpath)
    embedding_function = OpenAIEmbeddings()
    stores = Chroma(persist_directory=dirpath, embedding_function=embedding_function)

    template = """
        You are a creative AI assistant whose purpose is to perform data augmentation on a given set of data. 
        You will need to retrieve some data from the vector store, and use this information to generate a *list* of one or more entries of new data, with each entry having the following structure:
        
        {model}
        
        As much as possible, try to make the augmented data similar to but distinct from existing entries in the vector store. 
        
        You should try to generate new data that belong to different categories, instead of being fixated on just one category. 
        
        Context: {context}
        Description: {description}
    """
    parser = JsonOutputParser(pydantic_object=model)

    retriever = stores.as_retriever(search_type="mmr", search_kwargs={"fetch_k": 60, "k": 30})
    prompt = ChatPromptTemplate.from_messages(["human", template])

    rag_chain = (
        {
            "context": retriever,
            "description": RunnablePassthrough(),
            "model": lambda _: json.dumps({property: "str" for property in model.schema().get("properties")}, indent=2),
        }
        | prompt
        | llm
        | parser
    )

    iter_count = min(iter_count, MAX_ROWS)
    results = []

    for _ in range(iter_count):
        try:
            result = rag_chain.invoke(input)
            if isinstance(result, list) and result:
                results.extend(result)
            else:
                print(f"Invalid JSON output: {result}")
        except Exception as e:
            print(f"Error parsing result: {e}")
            continue

    if results:
        append_to_csv(filepath, data=results)

    split_dir = "/".join(split[:-1])
    response = supabase.storage.from_(f"synthesize_data/{split_dir}").upload(file=open(filepath, 'rb'), path="generated.csv")

    return results
def append_to_csv(filepath, data):
    print("Appending to CSV")
    with open(filepath, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        if file.tell() == 0:
            writer.writeheader()
        for row in data: 
            writer.writerow(row)

def embed_data(filepath, dirpath):
    with open(filepath, "rb") as file:
        raw_data = file.read()
        encoding = chardet.detect(raw_data)["encoding"]

    df = pd.read_csv(filepath, encoding=encoding, nrows=0)
    fieldnames = list(df.columns)
    fields = {field: (str, ...) for field in fieldnames}
    model = create_model("CSVModel", **fields)
    print("before loader")
    loader = CSVLoader(file_path=filepath, csv_args={"delimiter": ",", "quotechar": '"', "fieldnames": fieldnames})
    print("after loader")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    _ = Chroma.from_documents(documents=chunks, embedding=OpenAIEmbeddings(), persist_directory=dirpath)

    return model

args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 6, 23),
}

with DAG(
    default_args={
        'owner': 'RCH4CKERS',
        'retries': 1,
        'retry_delay': timedelta(minutes=5)
    },
    description='Synthesize Data',
    schedule_interval='@daily',
    start_date=datetime(2024, 6, 20),
    dag_id='synthesize_data',
) as dag:
    start = DummyOperator(task_id='start')
    fetch_data = PythonOperator(task_id='retrieve_and_augment_data', python_callable=retrieve_and_augment_data)
    end = DummyOperator(task_id='end')

    start >> fetch_data >> end
