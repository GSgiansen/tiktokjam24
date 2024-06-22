"use client";

import { Button } from "@/components/ui/button";
import { Form } from "@/components/ui/form";
import { useMultiplestepForm } from "@/hooks/useMultiplestepForm";
import { FormItems } from "@/types/formItems";
import { AnimatePresence, motion } from "framer-motion";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { formSchema } from "@/components/upload/form-schema";
import { z } from "zod";
import SideBar from "@/components/SideBar";
import FormStep from "@/components/upload/form-step";
import UploadStep from "@/components/upload/upload-step";
import ColumnStep from "@/components/upload/column-step";

const UploadPage = () => {
  const initialValues: FormItems = {
    name: "",
    email: "",
    phone: "",
    plan: "arcade",
    yearly: false,
  };
  const [formData, setFormData] = useState(initialValues);

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
  } = useMultiplestepForm(4);
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: "",
      email: "",
      phone: "",
      plan: "arcade",
      yearly: false,
    },
  });
  function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (Object.values(errors).some((error) => error)) {
      return;
    }
    nextStep();
  }
  function updateForm(fieldToUpdate: Partial<FormItems>) {
    const { name, email, phone } = fieldToUpdate;

    if (name && name.trim().length < 3) {
      setErrors((prevState) => ({
        ...prevState,
        name: "Name should be at least 3 characters long",
      }));
    } else if (name && name.trim().length > 15) {
      setErrors((prevState) => ({
        ...prevState,
        name: "Name should be no longer than 15 characters",
      }));
    } else {
      setErrors((prevState) => ({
        ...prevState,
        name: "",
      }));
    }

    if (email && !/\S+@\S+\.\S+/.test(email)) {
      setErrors((prevState) => ({
        ...prevState,
        email: "Please enter a valid email address",
      }));
    } else {
      setErrors((prevState) => ({
        ...prevState,
        email: "",
      }));
    }

    if (phone && !/^[0-9]{10}$/.test(phone)) {
      setErrors((prevState) => ({
        ...prevState,
        phone: "Please enter a valid 10-digit phone number",
      }));
    } else {
      setErrors((prevState) => ({
        ...prevState,
        phone: "",
      }));
    }

    setFormData({ ...formData, ...fieldToUpdate });
  }
  return (
    <div className="flex flex-row gap-3 p-4">
      <SideBar currentStepIndex={currentStepIndex} goTo={goTo} />
      <div className="grow">
        <Form {...form}>
          <form onSubmit={onSubmit} className="flex flex-col gap-4">
            <AnimatePresence mode="wait">
              {currentStepIndex === 0 && <FormStep {...formData} form={form} />}
              {currentStepIndex === 1 && (
                <UploadStep {...formData} form={form} />
              )}
              {currentStepIndex === 2 && (
                <div>
                  <ColumnStep {...formData} form={form} />
                </div>
              )}
              {currentStepIndex === 3 && <div>3</div>}
              {currentStepIndex === 4 && <div>4</div>}
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
