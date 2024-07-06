import BlurIn from "@/components/magicui/blur-in";
import { NeonGradientCard } from "@/components/magicui/neon-gradient-card";
import ShimmerButton from "@/components/magicui/shimmer-button";
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
    <div className="flex-1 w-full flex flex-col gap-20 items-center justify-center p-8">
      <WordPullUp words="Simplify Machine Learning!" />
      <BlurIn word="Just upload your CSV and tell us what to predict!!" />
      <Link href={"/upload"}>
        <ShimmerButton className="shadow-2xl">
          <span className="whitespace-pre-wrap text-center text-sm font-medium leading-none tracking-tight text-white dark:from-white dark:to-slate-900/10 lg:text-lg">
            Get Started Now
          </span>
        </ShimmerButton>
      </Link>
      <div className="flex flex-row gap-8 h-60">
        <NeonGradientCard className="max-w-sm items-center justify-center text-center">
          <span className="pointer-events-none z-10 h-full whitespace-pre-wrap bg-gradient-to-br from-[#ff2975] from-35% to-[#00FFF1] bg-clip-text text-center text-6xl font-bold leading-none tracking-tighter text-transparent dark:drop-shadow-[0_5px_5px_rgba(0,0,0,0.8)]">
            Text Synthesis
          </span>
        </NeonGradientCard>
        <NeonGradientCard className="max-w-sm items-center justify-center text-center">
          <span className="pointer-events-none z-10 h-full whitespace-pre-wrap bg-gradient-to-br from-[#ff2975] from-35% to-[#00FFF1] bg-clip-text text-center text-6xl font-bold leading-none tracking-tighter text-transparent dark:drop-shadow-[0_5px_5px_rgba(0,0,0,0.8)]">
            Automatic Model Creation
          </span>
        </NeonGradientCard>
      </div>
    </div>
  );
}
