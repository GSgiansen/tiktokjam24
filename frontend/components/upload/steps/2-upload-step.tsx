import { useEffect, useState } from "react";
import { Input } from "../../ui/input";
import { Label } from "../../ui/label";
import { StepProps } from "../step-props";
import { RadioGroup, RadioGroupItem } from "../../ui/radio-group";
import { Checkbox } from "../../ui/checkbox";
import { Spinner } from "../../ui/spinner";
import { Controller } from "react-hook-form";

const UploadStep = ({
  name,
  csvFile,
  columns,
  targetColumn,
  form,
  updateForm,
}: StepProps) => {
  const [selectColumns, setSelectColumns] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const { setValue, control } = form;
  const [selectedFile, setSelectedFile] = useState<File>();
  const onChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target?.files?.[0];
    if (file) {
      if (file.type === "text/csv" || file.name.endsWith(".csv")) {
        setSelectedFile(file);
        const formData = new FormData();
        formData.append("file", file);
        updateForm({ csvFile: file });
        try {
          setLoading(true);
          const response = await fetch("/api", {
            method: "POST",
            body: formData,
          });
          const data = await response.json();
          setLoading(false);
          setSelectColumns(data.headers);
        } catch (err) {
          console.error(err);
        }
      } else {
        alert("Invalid file type");
        console.error("Invalid file type");
      }
    } else {
      console.error("No file found");
    }
  };

  useEffect(() => {
    updateForm({ columns: selectColumns });
  }, [selectColumns]);

  useEffect(() => {
    console.log(csvFile);
    if (columns.length > 0) {
      setSelectColumns(columns);
    }
  }, []);

  return (
    <>
      <h2 className="text-2xl font-bold tracking-tight">Upload CSV File</h2>
      <p className="text-muted-foreground">Upload your CSV File here!</p>
      <div className="grid w-full max-w-sm items-center gap-1.5">
        <Label htmlFor="csvfile">CSV File</Label>
        <Controller
          name={"csvfile"}
          control={control}
          render={({ field: { value, ...field } }) => {
            return (
              <Input
                {...field}
                id="csvfile"
                type="file"
                onChange={onChange}
                value={value?.fileName}
              />
            );
          }}
        />
      </div>
      <div className="flex flex-row justify-around">
        {loading ? (
          <Spinner size="medium" />
        ) : (
          <>
            <div className="flex flex-col gap-2">
              <p className="font-bold">Columns</p>
              {selectColumns.map((column) => {
                return (
                  <div
                    key={column}
                    className="flex flex-row gap-2 items-center"
                  >
                    <li>{column}</li>
                  </div>
                );
              })}
            </div>
            <div>
              <p className="font-bold">Target</p>
              <RadioGroup
                defaultValue={targetColumn || ""}
                onValueChange={(value) => updateForm({ targetColumn: value })}
              >
                {selectColumns.map((column, index) => {
                  return (
                    <div
                      key={column}
                      className="flex flex-row items-center space-x-2 space-y-2"
                    >
                      <RadioGroupItem value={column} id={index.toString()} />
                      <Label htmlFor={index.toString()}>{column}</Label>
                    </div>
                  );
                })}
              </RadioGroup>
            </div>
          </>
        )}
      </div>
    </>
  );
};

export default UploadStep;
