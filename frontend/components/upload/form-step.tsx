import { FormItems } from "@/types/formItems";
import { Input } from "../ui/input";
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "../ui/form";
import { StepProps } from "./step-props";

const FormStep = ({ form }: StepProps) => {
  return (
    <div className="flex flex-col gap-4">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">Project Info</h2>
        <p className="text-muted-foreground">
          Enter your project info such as Project Name and details here!
        </p>
      </div>
      <FormField
        control={form.control}
        name="name"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Project Name</FormLabel>
            <FormControl>
              <Input placeholder="Project Name" {...field} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
    </div>
  );
};

export default FormStep;
