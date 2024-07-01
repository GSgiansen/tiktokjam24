import { StepProps } from "./step-props";

const SummaryStep = ({
  name,
  csvFile,
  columns,
  form,
  updateForm,
}: StepProps) => {
  console.log(name, csvFile, columns);
  return <>summary step</>;
};

export default SummaryStep;
