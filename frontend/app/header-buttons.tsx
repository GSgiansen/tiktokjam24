"use client";

import { Button } from "@tremor/react";
import { useRouter } from "next/navigation";
const HeaderButtons = () => {
  const router = useRouter();
  return (
    <Button
      onClick={() => {
        router.push("/");
      }}
    >
      Home
    </Button>
  );
};

export default HeaderButtons;
