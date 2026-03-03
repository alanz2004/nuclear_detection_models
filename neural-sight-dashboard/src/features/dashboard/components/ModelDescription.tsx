import { useModel } from "../../../context/ModelContext";
import { Settings } from "lucide-react";

export const ModelDescription = () => {
  const { selectedModel } = useModel();
  if (!selectedModel) return null;

  return (
    <div className="bg-gray-900 p-6 rounded-lg w-full md:w-1/2 flex flex-col gap-4">
      {/* Title with Icon */}
      <div className="flex items-center gap-2">
        <Settings size={20} className="text-white" />
        <h3 className="text-white font-semibold text-lg">Model Description</h3>
      </div>

      {/* Description */}
      <p className="text-sm text-gray-300">
        {selectedModel.description} This model is designed for time-series prediction with advanced LSTM architectures. 
        It uses sequential learning to capture temporal dependencies, and has been validated against multiple datasets to ensure robust performance. 
        Ideal for simulation, forecasting, and real-time analysis scenarios.
      </p>

      {/* Stats */}
      <div className="flex flex-col gap-1 text-sm mt-2">
        <span>
          Dropout Rate: <span className="text-blue-400">{selectedModel.dropoutRate}</span>
        </span>
        <span>
          Learning Rate: <span className="text-blue-400">{selectedModel.learningRate}</span>
        </span>
        <span>
          Number of Features: <span className="text-blue-400">{selectedModel.dataset.features.length}</span>
        </span>
        <span>
          Dataset Size: <span className="text-blue-400">{selectedModel.dataset.totalSize}</span>
        </span>
        <span>
          Dataset Source: <span className="text-blue-400">{selectedModel.dataset.source}</span>
        </span>
      </div>
    </div>
  );
};