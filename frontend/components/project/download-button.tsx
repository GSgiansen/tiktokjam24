import React from "react";
import { Button } from "../ui/button";

interface DownloadButtonProps {
  downloadUrl: string;
}

const DownloadButton: React.FC<DownloadButtonProps> = ({ downloadUrl }) => {
  const handleDownload = () => {
    // URL of the file to be downloaded
    const fileUrl = downloadUrl;
    const fileName = "result.csv";

    // Fetch the file from the URL
    fetch(fileUrl)
      .then((response) => response.blob())
      .then((blob) => {
        // Create a link element
        const link = document.createElement("a");
        link.href = window.URL.createObjectURL(blob);
        link.download = fileName;

        // Append the link to the document body
        document.body.appendChild(link);

        // Programmatically click the link to trigger the download
        link.click();

        // Remove the link from the document
        document.body.removeChild(link);
      })
      .catch((error) => {
        console.error("Error downloading the file", error);
      });
  };

  return (
    <Button
      onClick={handleDownload}
      className="btn btn-primary bg-blue-500 text-white p-2 rounded-md"
    >
      Download File
    </Button>
  );
};

export default DownloadButton;
