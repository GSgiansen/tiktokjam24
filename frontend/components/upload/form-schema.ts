"use client";

import { z } from "zod";

export const formSchema = z.object({
  name: z.string().min(2).max(50),
  email: z.string().max(50),
  phone: z.string().min(2).max(50),
  plan: z.string().min(2).max(50),
  yearly: z.boolean(),
});
