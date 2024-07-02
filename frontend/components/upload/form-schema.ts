"use client";

import { z } from "zod";

export const formSchema = z.object({
  name: z.string().min(2).max(50),
  csvFile: z.any().refine((val) => val.length > 0, "File is required"),
  columns: z.array(z.string()),
});
