"use client";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import MetricsComponent from "@/components/project/metrics";
import ShineBorder from "@/components/magicui/shine-border";
import { createClient } from "@/utils/supabase/client";
import FileUploader from "@/components/project/predict";
import Predict from "@/components/project/predict";
import { useEffect, useState } from "react";

type Project = {
  id: string;
  name: string;
  owner: string;
  ml_method: string;
  features: [string];
};
export default function Page({ params }: { params: { id: string } }) {
  const supabase = createClient();
  const [project, setProject] = useState<Project | null>(null);
  useEffect(() => {
    fetch(
      `http://128.199.130.222:8000/projects/project?project_id=${params.id}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    )
      .then((res) => res.json())
      .then((data) => {
        console.log(data.data[0]);
        setProject(data.data[0]);
      });
  }, []);

  return (
    <div className="p-6 border-4 border-gray-300 rounded-lg shadow-lg max-w-md mx-auto">
      <div>
        <p>
          <strong>Project: </strong>
          {project?.name}
        </p>
        <p className="capitalize">
          <strong>ML Method:</strong> {project?.ml_method}
        </p>
      </div>

      <br />
      <Tabs defaultValue="account" className="w-[400px]">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="account">Start Training</TabsTrigger>
          <TabsTrigger value="metrics">Metrics</TabsTrigger>
          <TabsTrigger value="predict">Predict</TabsTrigger>
        </TabsList>
        <TabsContent value="account">
          <div className="flex items-center justify-center p-4">
            <button>
              <ShineBorder
                className="text-center text-2xl font-bold capitalize"
                color={["#A07CFE", "#FE8FB5", "#FFBE7B"]}
              >
                <div
                  onClick={() => {
                    supabase.auth.getSession().then(({ data: { session } }) => {
                      fetch(`http://128.199.130.222:8000/trigger_dag/`, {
                        method: "POST",
                        headers: {
                          "Content-Type": "application/json",
                          Authorization: `Bearer ${session?.access_token}`, // Include your authorization token
                        },
                        body: JSON.stringify({
                          dag_id: "ml_pipeline",
                          conf: {
                            project_id: params.id,
                          },
                        }),
                      });
                    });
                  }}
                >
                  Start
                </div>
              </ShineBorder>
            </button>
          </div>
        </TabsContent>
        <TabsContent value="metrics">
          <MetricsComponent id={params.id} mlMethod={project?.ml_method} />
        </TabsContent>
        <TabsContent value="predict">
          <>
            {/* Upload CSV (project-id/add_predict.csv) dag_id:
            "add_predict_pipeline", conf { project_id: params.id } 
            check projects table additional_predict field if its true or not
            result file: project-id/data/add_predict_res.csv
            */}
          </>
          <Predict project_id={params.id} />
        </TabsContent>
      </Tabs>
    </div>
  );
}
