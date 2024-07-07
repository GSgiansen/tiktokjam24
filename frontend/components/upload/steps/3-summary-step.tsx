import { RiCheckboxCircleLine } from "@remixicon/react";
import { StepProps } from "../step-props";

const SummaryStep = ({
  name,
  csvFile,
  columns,
  ml_method,
  targetColumn,
  form,
  updateForm,
}: StepProps) => {
  console.log(name, csvFile, columns);
  return (
    <div className="bg-gray-800 text-white shadow-lg rounded-lg overflow-hidden">
      <div className="px-6 py-4">
        <h1 className="text-2xl font-bold mb-4">Project Summary</h1>

        {/* Project Name Section */}
        <div className="mb-4">
          <strong className="text-gray-400">Project Name:</strong>
          <p className="text-gray-100 ml-2">{name}</p>
        </div>

        {/* Uploaded File Section */}
        <div className="mb-4">
          <strong className="text-gray-400">Uploaded File:</strong>
          <p className="text-gray-100 ml-2">{csvFile?.name}</p>
        </div>

        {/* ML Method File Section */}
        <div className="mb-4">
          <strong className="text-gray-400">ML Method:</strong>
          <p className="text-gray-100 ml-2">{ml_method}</p>
        </div>

        {/* Columns Section */}
        <div className="rounded-lg shadow-lg max-w-md">
          <strong className="text-gray-400">Columns</strong>

          <div className="overflow-x-auto">
            <table className="min-w-full bg-white">
              <thead>
                <tr className="bg-gray-200">
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Column Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Target Column
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {columns.map((column, index) => (
                  <tr key={index}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {column}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {column === targetColumn && (
                        <RiCheckboxCircleLine className="text-green-500" />
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SummaryStep;
