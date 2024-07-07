"use client";

import { Button } from "@/components/ui/button";
import { Form } from "@/components/ui/form";
import { useMultiplestepForm } from "@/hooks/useMultiplestepForm";
import { FormItems } from "@/types/formItems";
import { AnimatePresence, motion } from "framer-motion";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { formSchema } from "@/components/upload/form-schema";
import { z } from "zod";
import SideBar from "@/components/SideBar";
import { createClient } from "@/utils/supabase/client";
import { redirect, useRouter } from "next/navigation";
import ProjectInfoStep from "@/components/upload/steps/1-project-info-step";
import UploadStep from "@/components/upload/steps/2-upload-step";
import SummaryStep from "@/components/upload/steps/3-summary-step";
import { Spinner } from "@/components/ui/spinner";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

const UploadPage = () => {
  const supabase = createClient();
  const [authenticated, setAuthenticated] = useState(false);
  const [accessToken, setAccessToken] = useState<string>("");
  useEffect(() => {
    const checkSession = async () => {
      const {
        data: { session },
      } = await supabase.auth.getSession();
      if (!session) {
        router.push("/login");
      } else {
        setAccessToken(session.access_token);
        setAuthenticated(true);
      }
    };
    checkSession();
  }, []);

  const initialValues: FormItems = {
    name: "",
    csvFile: undefined,
    columns: [],
    targetColumn: "",
    ml_method: "",
  };
  const [formData, setFormData] = useState(initialValues);
  const router = useRouter();
  const [isCreating, setIsCreating] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  const [errors, setErrors] = useState<Record<string, string>>({});
  const {
    previousStep,
    nextStep,
    currentStepIndex,
    isFirstStep,
    isLastStep,
    steps,
    goTo,
    showSuccessMsg,
  } = useMultiplestepForm(3);
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: "",
      csvFile: null,
      columns: [],
    },
  });
  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    if (isLastStep) {
      // setIsCreating(true);
      // setIsOpen(true);
      e.preventDefault();
      supabase.auth.getSession().then(({ data: { session } }) => {
        console.log(formData);
        const finalFormData = new FormData();
        finalFormData.append("name", formData.name);
        finalFormData.append("file", formData.csvFile);
        finalFormData.append("owner", session?.user.id);
        finalFormData.append("target", formData.targetColumn);
        finalFormData.append("columns", JSON.stringify(formData.columns));
        finalFormData.append("ml_method", formData.ml_method);
        console.log(finalFormData);
        fetch("http://127.0.0.1:8000/projects/project", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${accessToken}`, // Include your authorization token
          },
          body: finalFormData,
        })
          .then((response) => response.json())
          .then((data) => {
            setTimeout(() => {
              setIsCreating(false);
              // router.push(`/project/${data.id}`);
            }, 5000);
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      });
    } else {
      e.preventDefault();
      if (Object.values(errors).some((error) => error)) {
        return;
      }
      nextStep();
    }
  }
  function updateForm(fieldToUpdate: Partial<FormItems>) {
    const { name, csvFile, columns, targetColumn } = fieldToUpdate;
    console.log("updating", fieldToUpdate);
    setFormData({ ...formData, ...fieldToUpdate });
  }

  if (!authenticated) {
    return <Spinner />;
  }

  return (
    <div className="flex flex-row gap-3 p-4">
      <SideBar currentStepIndex={currentStepIndex} goTo={goTo} />
      <Dialog open={isOpen} className="max-w-md mx-auto">
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Creating your project...</DialogTitle>
            <DialogDescription>
              <Spinner />
            </DialogDescription>
          </DialogHeader>
        </DialogContent>
      </Dialog>

      <div className="grow">
        <Form {...form}>
          <form onSubmit={onSubmit} className="flex flex-col gap-4">
            <AnimatePresence mode="wait">
              {currentStepIndex === 0 && (
                <ProjectInfoStep
                  {...formData}
                  form={form}
                  updateForm={updateForm}
                />
              )}
              {currentStepIndex === 1 && (
                <UploadStep {...formData} form={form} updateForm={updateForm} />
              )}
              {currentStepIndex === 2 && (
                <SummaryStep
                  {...formData}
                  form={form}
                  updateForm={updateForm}
                />
              )}
            </AnimatePresence>
            <div className="w-full items-center flex justify-between ">
              <Button
                onClick={previousStep}
                type="button"
                variant="ghost"
                className={`${
                  isFirstStep
                    ? "invisible"
                    : "visible p-0 text-neutral-200 hover:text-white"
                }`}
              >
                Go Back
              </Button>
              <div className="relative after:pointer-events-none after:absolute after:inset-px after:rounded-[11px] after:shadow-highlight after:shadow-white/10 focus-within:after:shadow-[#77f6aa] after:transition">
                <Button
                  disabled={isCreating}
                  type="submit"
                  className="relative text-neutral-200 bg-neutral-900 border border-black/20 shadow-input shadow-black/10 rounded-xl hover:text-white"
                >
                  {isLastStep ? "Confirm" : "Next Step"}
                </Button>
              </div>
            </div>
          </form>
        </Form>
      </div>
    </div>
  );
};

export default UploadPage;
