import ShineBorder from "@/components/magicui/shine-border";
import { createClient } from "@/utils/supabase/server";
import { Card } from "@tremor/react";
import Link from "next/link";
import { redirect } from "next/navigation";

const DashboardPage = async () => {
  const supabase = createClient();
  const supabaseAuth = await supabase.auth.getUser();
  const userId = supabaseAuth.data.user?.id;
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    return redirect("/login");
  }

  try {
    const response = await fetch(
      `http://128.199.130.222:8000/projects/queryProjects?owner=${userId}`,
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
      <div className="flex justify-center flex-col gap-4 p-4">
        <h1 className="font-bold text-4xl">Projects</h1>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {projects.data.map((data: any) => (
            <Link key={data.id} href={`/project/${data.id}`}>
              <div className="p-4 border-4 border-gray-300 rounded-lg shadow-lg transform transition-transform duration-300 hover:border-blue-500">
                <div className="text-xl font-bold">{data.name}</div>
                <div className="text-gray-600 capitalize">{data.ml_method}</div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    );
  } catch (error) {
    console.log(error);
  }
};

export default DashboardPage;
