import { FaSpinner } from "react-icons/fa";

export function Loading() {
  return (
    <div className="flex items-center justify-center">
      <div className="flex flex-col items-center space-y-4 text-gray-600">
        <FaSpinner className="animate-spin text-4xl text-blue-500" />
        <p className="text-lg font-medium">Loading, please wait...</p>
      </div>
    </div>
  );
}