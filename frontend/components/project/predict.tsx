import React, { useEffect, useState } from "react";
import { Input } from "../ui/input";
import { Button } from "../ui/button";
import { Spinner } from "../ui/spinner";
import { createClient } from "@/utils/supabase/client";

type FileUploaderProps = {
  project_id: string;
};

const FileUploader = ({ project_id }: FileUploaderProps) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [fileExist, setFileExist] = useState(false);
  const [loading, setLoading] = useState(false);
  const supabase = createClient();

  useEffect(() => {
    setLoading(true);
    fetch(
      `http://127.0.0.1:8000/projects/checkPredictFileExist?project_id=${project_id}`
    )
      .then((response) => {
        setLoading(false);
        console.log(response.status);
        if (response.status === 200) {
          console.log("file exist");
          setFileExist(true);
        }
        return response.json();
      })
      .then((data) => {
        console.log(data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  const handleFileChange = (event: any) => {
    const file = event.target.files[0];
    if (file && file.type === "text/csv") {
      setSelectedFile(file);
      setErrorMessage("");
    } else {
      setSelectedFile(null);
      setErrorMessage("Please select a CSV file.");
    }
  };

  const handleUpload = () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append("project_id", project_id);
      formData.append("file", selectedFile);

      supabase.auth.getSession().then(({ data: { session } }) => {
        fetch("http://127.0.0.1:8000/projects/uploadPredict", {
          method: "POST",
          body: formData,
          headers: {
            Authorization: `Bearer ${session?.access_token}`,
          },
        })
          .then((response) => response.json())
          .then((data) => {
            console.log("Upload success:", data);
            // Reset selected file after upload
            setSelectedFile(null);
          })
          .catch((error) => {
            console.error("Error uploading file:", error);
          });
      });
    }
  };

  return (
    <div className="p-4 shadow-md rounded-md">
      {loading ? (
        <div className="flex items-center justify-center">
          <Spinner /> {/* Replace with your Spinner component */}
        </div>
      ) : fileExist ? (
        <>
          <Button
            onClick={() => {
              supabase.auth.getSession().then(({ data: { session } }) => {
                fetch(`http://127.0.0.1:8000/trigger_dag/`, {
                  method: "POST",
                  headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${session?.access_token}`, // Include your authorization token
                  },
                  body: JSON.stringify({
                    dag_id: "ml_pipeline",
                    conf: {
                      project_id: project_id,
                    },
                  }),
                });
              });
            }}
          >
            Start Prediction Job
          </Button>
        </>
      ) : (
        <>
          <Input
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            className="mb-4"
          />
          {errorMessage && <p className="text-red-500 mb-4">{errorMessage}</p>}
          <Button
            onClick={handleUpload}
            className={`bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded ${
              selectedFile ? "" : "opacity-50 cursor-not-allowed"
            }`}
            disabled={!selectedFile}
          >
            Upload File
          </Button>
        </>
      )}
    </div>
  );
};

export default FileUploader;
