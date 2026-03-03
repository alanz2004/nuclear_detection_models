import { useModel } from "../../../context/ModelContext";
import { Database, Hash, FileText, Activity } from "lucide-react";

export const DatasetMetadata = () => {
  const { selectedModel } = useModel();
  if (!selectedModel) return null;

  const { dataset } = selectedModel;

  return (
    <div className="bg-gray-900 p-8 rounded-lg w-full md:w-1/3 flex flex-col gap-6">
      {/* Title with Icon */}
      <div className="flex items-center gap-3 mb-4">
        <Database size={22} className="text-white" />
        <h3 className="text-white font-semibold text-lg">Dataset Metadata</h3>
      </div>

      {/* Total Size */}
      <div className="flex items-start gap-3">
        <Hash size={16} className="text-gray-400 mt-1" />
        <div className="flex flex-col gap-2">
          <span className="text-gray-400 text-sm">Total Size</span>
          <span className="text-blue-400 font-semibold">{dataset.totalSize}</span>
        </div>
      </div>


      {/* Source */}
      <div className="flex items-start gap-3">
        <Activity size={16} className="text-gray-400 mt-1" />
        <div className="flex flex-col gap-2">
          <span className="text-gray-400 text-sm">Source</span>
          <span className="text-blue-400 font-semibold">{dataset.source}</span>
        </div>
      </div>

      {/* Distribution Balance */}
      <div className="flex flex-col gap-2">
        <span className="text-gray-400 text-sm">Distribution Balance</span>
        <div className="w-full h-4 bg-gray-800 rounded">
          <div
            className="h-4 bg-blue-500 rounded"
            style={{ width: `${dataset.accidentPercentage}%` }}
          />
        </div>
      </div>
    </div>
  );
};