import AuthButton from "@/components/AuthButton";
import ModeToggle from "@/components/mode-toggle";
import { Button } from "@/components/ui/button";
import { createClient } from "@/utils/supabase/server";
import Link from "next/link";
import HeaderButtons from "./header-buttons";

export async function SiteHeader() {
  const supabase = createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  return (
    <header className="sticky top-0 z-50 py-1 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-14 max-w-screen-2xl items-center px-4 gap-8">
        <Link href={"/"}>
          <p>Home</p>
        </Link>
        {user && (
          <>
            <Link href="/dashboard">
              <p>Dashboard</p>
            </Link>
            <Link href="/upload">
              <p>Upload</p>
            </Link>
          </>
        )}
        <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
          <nav className="flex items-center gap-4">
            <AuthButton />
            {/* <ModeToggle /> */}
          </nav>
        </div>
      </div>
    </header>
  );
}
