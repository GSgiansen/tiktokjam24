import { FormItems } from "@/types/formItems";

export type StepProps = FormItems & {
  form: any;
  updateForm: (fieldToUpdate: Partial<FormItems>) => void;
};
