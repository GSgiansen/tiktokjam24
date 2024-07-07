import { useEffect, useState } from "react";
import FileUploader from "./file-upload";

const PredictStatus = ({
  status,
  project_id,
}: {
  status: boolean;
  project_id: string;
}) => {
  const [jobRunning, setJobRunning] = useState<boolean>(false);
  const fetchData = async () => {
    console.log("fetching");
    try {
      const response = await fetch(
        `http://128.199.130.222:8080/projects/checkPredictResultFileExist?project_id=${project_id}`
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      console.log(result);
      setJobRunning(true);
    } catch (error: any) {}
  };

  console.log(status);
  useEffect(() => {
    fetchData(); // Fetch data immediately when component mounts
    const intervalId = setInterval(fetchData, 5000); // Fetch data every 5 seconds

    return () => clearInterval(intervalId); // Cleanup interval on component unmount
  }, []);

  return (
    <div className="p-4 shadow-md rounded-md">
      {status === true && (
        <div className="p-4 bg-green-100 text-green-800">
          {jobRunning ? <>t</> : <>f</>}
        </div>
      )}
      {status === false && <FileUploader project_id={project_id} />}
    </div>
  );
};

export default PredictStatus;
