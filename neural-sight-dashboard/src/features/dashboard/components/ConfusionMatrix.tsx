import { useModel } from "../../../context/ModelContext";
import { Activity } from "lucide-react";

export const ConfusionMatrix = () => {
  const { selectedModel } = useModel();
  if (!selectedModel) return null;

  const { confusionMatrix } = selectedModel;

  return (
    <div className="bg-gray-900 p-8 rounded-lg w-full md:w-1/2 flex flex-col gap-6">
      {/* Title with Icon */}
      <div className="flex items-center gap-3 mb-6">
        <Activity size={22} className="text-white" />
        <h3 className="text-white font-bold text-xl">Confusion Matrix</h3>
      </div>

      {/* Matrix Grid */}
      <div className="grid grid-cols-2 gap-x-3 gap-y-6">
        {/* True Positive */}
        <div className="bg-blue-500 py-6 rounded text-center text-white font-semibold">
          {confusionMatrix[0][0]}
          <br />
          True Positive
        </div>

        {/* False Positive */}
        <div className="bg-gray-800 py-6 rounded text-center text-white font-semibold">
          {confusionMatrix[0][1]}
          <br />
          False Positive
        </div>

        {/* False Negative */}
        <div className="bg-gray-800 py-6 rounded text-center text-white font-semibold">
          {confusionMatrix[1][0]}
          <br />
          False Negative
        </div>

        {/* True Negative */}
        <div className="bg-green-500 py-6 rounded text-center text-white font-semibold">
          {confusionMatrix[1][1]}
          <br />
          True Negative
        </div>
      </div>
    </div>
  );
};