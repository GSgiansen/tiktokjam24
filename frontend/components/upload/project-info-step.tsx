import { Input } from "../ui/input";
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "../ui/form";
import { StepProps } from "./step-props";

const ProjectInfoStep = ({ name, form, updateForm }: StepProps) => {
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
              <Input
                autoFocus
                type="text"
                id="name"
                placeholder="Project Name"
                {...field}
                value={name}
                onChange={(e) => updateForm({ name: e.target.value })}
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
    </div>
  );
};

export default ProjectInfoStep;
