import AuthButton from "@/components/AuthButton";
import ModeToggle from "@/components/mode-toggle";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-50 py-1 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-14 max-w-screen-2xl items-center px-4 gap-8">
        <Link href={"/"}>
          <Button>Home</Button>
        </Link>
        <Link href={"/dashboard"}>
          <Button>Dashboard</Button>
        </Link>
        <Link href={"/upload"}>
          <Button>Upload</Button>
        </Link>
        <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
          <nav className="flex items-center gap-4">
            <AuthButton />
            <ModeToggle />
          </nav>
        </div>
      </div>
    </header>
  );
}
