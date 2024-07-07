import {
  RiCheckboxCircleLine,
  RiTimerLine,
  RiInformationLine,
} from "@remixicon/react";
import React, { useEffect, useState } from "react";

type MetricsComponentProps = {
  id: string;
  mlMethod: string | undefined;
};

type ClassificationModel = {
  data: {
    loss?: number;
    accuracy?: number;
    created_at: string;
    name: string;
    epoch: number;
  }[];
};

const MetricsComponent = ({ id, mlMethod }: MetricsComponentProps) => {
  const [details, setDetails] = useState<ClassificationModel>({
    data: [],
  });
  const metric = mlMethod === "classification" ? "Accuracy" : "Loss";

  useEffect(() => {
    const fetchDetails = async () => {
      const method: string =
        mlMethod === "classification"
          ? "classification_models"
          : "regression_models";

      const path: string =
        mlMethod === "classification"
          ? "classification_model"
          : "regression_model";
      console.log(method, path);
      try {
        const response = await fetch(
          `http://128.199.130.222:8000/${method}/${path}?project_id=${id}`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        setDetails(data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchDetails();
  }, [id]);

  if (!details) {
    return <div>Loading...</div>;
  }

  // Check if details.data exists and has at least one element
  if (!details.data || details.data.length === 0) {
    return (
      <div className="flex items-center justify-center p-4">
        <div className="flex items-center  gap-4 rounded-lg">
          <RiInformationLine className="text-blue-500 text-4xl" />
          <div>
            <p className="text-lg font-semibold">No data found!</p>
            <p className="text-gray-600">Have you started the job?</p>
          </div>
        </div>
      </div>
    );
  }

  // Now safely access details.data[0]
  const model = details.data[0];

  return (
    <div className="p-6 border-4 border-gray-300 rounded-lg shadow-lg max-w-md mx-auto">
      <h2 className="text-2xl font-bold mb-4">{model.name}</h2>
      <div className="flex items-center mb-4">
        <RiCheckboxCircleLine className="text-green-500 mr-2" />
        <span className="text-lg font-medium">
          {metric}: {mlMethod == "classification" ? model.accuracy : model.loss}
          %
        </span>
      </div>
      <div className="flex items-center mb-4">
        <RiTimerLine className="text-gray-500 mr-2" />
        <span className="text-lg font-medium">
          Created: {new Date(model.created_at).toLocaleString()}
        </span>
      </div>
      {mlMethod === "regression" && (
        <div className="flex items-center">
          <RiTimerLine className="text-gray-500 mr-2" />
          <span className="text-lg font-medium">Epochs: {model.epoch}</span>
        </div>
      )}
    </div>
  );
};

export default MetricsComponent;
