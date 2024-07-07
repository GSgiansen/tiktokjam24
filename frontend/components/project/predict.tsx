import React, { useEffect, useState } from "react";
import { Spinner } from "../ui/spinner";
import { createClient } from "@/utils/supabase/client";
import PredictStatus from "./predict-status";

type PredictProps = {
  project_id: string;
};

const Predict = ({ project_id }: PredictProps) => {
  const [loading, setLoading] = useState(false);
  const [additionalPredict, setAdditionalPredict] = useState<boolean>(false);
  const supabase = createClient();

  useEffect(() => {
    setLoading(true);
    fetch(
      `http://128.199.130.222:8080/projects/checkPredictFileExist?project_id=${project_id}`
    )
      .then((response) => {
        console.log(response.status);
        if (response.status == 200) {
          setAdditionalPredict(true);
        }
        setLoading(false);
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
      {loading ? (
        <div className="flex items-center justify-center">
          <Spinner /> {/* Replace with your Spinner component */}
        </div>
      ) : (
        <>
          <PredictStatus status={additionalPredict} project_id={project_id} />
        </>
      )}
    </div>
  );
};

export default Predict;
