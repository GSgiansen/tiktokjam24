export type FormItems = {
  name: string;
  csvFile: Blob | null;
  columns: string[];
  targetColumn: string;
  ml_method: string;
};
