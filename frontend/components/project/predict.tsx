import React, { useState } from "react";
import { Input } from "../ui/input";
import { Button } from "../ui/button";

type FileUploaderProps = {
  project_id: string;
};

const FileUploader = ({ project_id }: FileUploaderProps) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");

  const handleFileChange = (event) => {
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
      formData.append("file", selectedFile);

      fetch("http://127.0.0.1:8000/projects/uploadPredict", {
        method: "POST",
        body: formData,
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
        className={`bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded ${
          selectedFile ? "" : "opacity-50 cursor-not-allowed"
        }`}
        disabled={!selectedFile}
      >
        Upload File
      </Button>
    </div>
  );
};

export default FileUploader;
