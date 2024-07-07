import React, { useEffect, useState } from "react";
import { createClient } from "@/utils/supabase/client";
import PredictStatus from "./predict-status";
import { Button } from "../ui/button";

type PredictProps = {
  project_id: string;
};

const Predict = ({ project_id }: PredictProps) => {
  const [additionalPredict, setAdditionalPredict] = useState<boolean>(false);
  const [downloadUrl, setDownloadUrl] = useState<string>("");
  const supabase = createClient();

  useEffect(() => {
    fetch(
      `http://128.199.130.222:8000/projects/checkPredictFileExist?project_id=${project_id}`
    )
      .then((response) => {
        console.log(response.status);
        if (response.status == 200) {
          setAdditionalPredict(true);
        }
        return response.json();
      })
      .then((data) => {
        console.log(data);
      })
      .catch((error) => {
        console.log(error);
      });

    supabase.auth.getSession().then(({ data: { session } }) => {
      console.log(session);
    });
  }, []);

  return (
    <div className="p-4 shadow-md rounded-md">
      <>
        <PredictStatus status={additionalPredict} project_id={project_id} />
      </>
    </div>
  );
};

export default Predict;
