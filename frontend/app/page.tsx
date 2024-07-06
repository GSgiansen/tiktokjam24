import BlurIn from "@/components/magicui/blur-in";
import WordPullUp from "@/components/magicui/word-pull-up";
import { Button } from "@/components/ui/button";
import { createClient } from "@/utils/supabase/server";
import Link from "next/link";

export default function Home() {
  const canInitSupabaseClient = () => {
    // This function is just for the interactive tutorial.
    // Feel free to remove it once you have Supabase connected.
    try {
      createClient();
      return true;
    } catch (e) {
      return false;
    }
  };

  const isSupabaseConnected = canInitSupabaseClient();

  return (
    <div className="flex-1 w-full flex flex-col gap-20 items-start p-8">
      <WordPullUp words="Simplify Machine Learning!" />
      <BlurIn word="Just upload your CSV and tell us what to predict!!" />
      <Link href={"/dashboard"}>
        <Button>Get Started Now</Button>
      </Link>
    </div>
  );
}
