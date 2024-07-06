import {
  RiCheckboxCircleLine,
  RiTimerLine,
  RiInformationLine,
} from "@remixicon/react";
import React, { useEffect, useState } from "react";

type MetricsComponentProps = {
  id: string;
};

const MetricsComponent = ({ id }: MetricsComponentProps) => {
  const [details, setDetails] = useState(null);

  useEffect(() => {
    const fetchDetails = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/classification_models/classification_model?project_id=${id}`,
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
        <span className="text-lg font-medium">Accuracy: {model.accuracy}%</span>
      </div>
      <div className="flex items-center">
        <RiTimerLine className="text-gray-500 mr-2" />
        <span className="text-lg font-medium">
          Created: {new Date(model.created_at).toLocaleString()}
        </span>
      </div>
    </div>
  );
};

export default MetricsComponent;
