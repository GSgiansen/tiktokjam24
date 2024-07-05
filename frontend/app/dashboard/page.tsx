import { createClient } from "@/utils/supabase/server";
import { Card } from "@tremor/react";
import Link from "next/link";

const DashboardPage = async () => {
  const supabase = createClient();
  const supabaseAuth = await supabase.auth.getUser();
  const userId = supabaseAuth.data.user?.id;
  try {
    const response = await fetch(
      `http://127.0.0.1:8000/projects/queryProjects?owner=${userId}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    const projects = await response.json();
    console.log(projects);
    return (
      <div className="flex flex-col gap-4">
        {projects.data.map((data: any) => {
          return (
            <Link href={`/project/${data.id}`}>
              <Card>
                <div className="flex flex-col border-gray-500 border-4 rounded-2xl hover:border-white">
                  {data.name}
                </div>
              </Card>
            </Link>
          );
        })}
      </div>
    );
  } catch (error) {
    console.log(error);
  }
};

export default DashboardPage;
