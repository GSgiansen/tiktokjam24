import React, { useState } from "react";
import { Input } from "../ui/input";
import { Button } from "../ui/button";
import { Spinner } from "../ui/spinner";
import { createClient } from "@/utils/supabase/client";

const FileUploader = ({ project_id }: { project_id: string }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const supabase = createClient();

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === "text/csv") {
      setSelectedFile(file);
      setErrorMessage("");
    } else {
      setSelectedFile(null);
      setErrorMessage("Please select a CSV file.");
    }
  };

  const handleUpload = async () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append("project_id", project_id);
      formData.append("file", selectedFile);

      setIsUploading(true);

      try {
        supabase.auth.getSession().then(({ data: { session } }) => {
          fetch("http://128.199.130.222:8080/projects/uploadPredict", {
            method: "POST",
            body: formData,
            headers: {
              Authorization: `Bearer ${session?.access_token}`,
            },
          })
            .then((response) => response.json())
            .then((data) => {
              {
                fetch(`http://128.199.130.222:8000/trigger_dag/`, {
                  method: "POST",
                  headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${session?.access_token}`, // Include your authorization token
                  },
                  body: JSON.stringify({
                    dag_id: "add_predict_pipeline",
                    conf: {
                      project_id: project_id,
                    },
                  }),
                });
              }
            })
            .catch((error) => {
              console.error("Error:", error);
            });
        });

        setSelectedFile(null);
      } catch (error) {
        console.error("Error uploading file:", error);
      } finally {
        setIsUploading(false);
      }
    }
  };

  return (
    <div className="p-4 shadow-md rounded-md">
      <Input
        type="file"
        accept=".csv"
        onChange={handleFileChange}
        className="mb-4"
      />
      {errorMessage && <p className="text-red-500 mb-4">{errorMessage}</p>}
      <Button
        onClick={handleUpload}
        disabled={!selectedFile || isUploading}
        className={`bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded ${
          !selectedFile || isUploading ? "opacity-50 cursor-not-allowed" : ""
        }`}
      >
        {isUploading ? <Spinner /> : "Upload File"}
      </Button>
    </div>
  );
};

export default FileUploader;
