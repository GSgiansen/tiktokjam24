import { StepProps } from "../step-props";

const SummaryStep = ({
  name,
  csvFile,
  columns,
  form,
  updateForm,
}: StepProps) => {
  console.log(name, csvFile, columns);
  return (
    <div className="flex flex-col">
      <div>{name}</div>
      <div>{csvFile?.name}</div>
      <div>{columns}</div>
    </div>
  );
};

export default SummaryStep;
