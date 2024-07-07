"use client";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import MetricsComponent from "@/components/project/metrics";
import ShineBorder from "@/components/magicui/shine-border";
export default function Page({ params }: { params: { id: string } }) {
  return (
    <div className="p-6 border-4 border-gray-300 rounded-lg shadow-lg max-w-md mx-auto">
      <Tabs defaultValue="account" className="w-[400px]">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="account">Start Training</TabsTrigger>
          <TabsTrigger value="metrics">Metrics</TabsTrigger>
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
                    fetch(`/trigger_dag/`, {
                      method: "POST",
                      headers: {
                        "Content-Type": "application/json",
                      },
                      body: JSON.stringify({
                        dag_id: "ml_pipeline",
                        conf: {
                          project_id: params.id,
                        },
                      }),
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
          <MetricsComponent id={params.id} />
        </TabsContent>
      </Tabs>
    </div>
  );
}
