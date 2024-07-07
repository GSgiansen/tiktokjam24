import { useEffect, useState } from "react";
import FileUploader from "./file-upload";
import { Button } from "../ui/button";
import DownloadButton from "./download-button";

const PredictStatus = ({
  status,
  project_id,
}: {
  status: boolean;
  project_id: string;
}) => {
  const [jobRunning, setJobRunning] = useState<boolean>(false);
  const [downloadUrl, setDownloadUrl] = useState<string>("");

  useEffect(() => {
    fetch(
      `http://127.0.0.1:8000/projects/getResultFileUrl?project_id=${project_id}`,
      {
        method: "GET",
      }
    )
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        setDownloadUrl(data.signedURL);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  return (
    <div className="p-4 shadow-md rounded-md">
      {status === true && (
        <div className="p-4 bg-green-100 text-green-800 text-center">
          <DownloadButton downloadUrl={downloadUrl} />
        </div>
      )}
      {status === false && <FileUploader project_id={project_id} />}
    </div>
  );
};

export default PredictStatus;
