import { useEffect } from "react";
import { Brain } from "lucide-react";
import { useModels } from "../hooks/useModels";
import { useModel } from "../../../context/ModelContext";

const ModelList = () => {
  const { models, loading, error } = useModels();
  const { selectedModel, setSelectedModel } = useModel();

  // Automatically select the first model when loaded
  useEffect(() => {
    if (!selectedModel && models.length > 0) {
      setSelectedModel(models[0]);
    }
  }, [models, selectedModel, setSelectedModel]);

  if (loading) {
    return <div className="text-sm text-gray-400">Loading models...</div>;
  }

  if (error) {
    return <div className="text-sm text-red-400">{error}</div>;
  }

  return (
    <div className="mt-6">
      <p className="text-xs text-gray-400 uppercase tracking-wider mb-3">
        Model Architectures
      </p>

      <div className="flex flex-col gap-2">
        {models.map((model) => {
          const isSelected = selectedModel?.id === model.id;

          return (
            <button
              key={model.id}
              onClick={() => setSelectedModel(model)}
              className={`flex items-center justify-between px-3 py-2 rounded-lg text-sm transition
                ${isSelected
                  ? "bg-blue-600 text-white"
                  : "text-gray-300 hover:bg-slate-700"
                }`}
            >
              <div className="flex items-center gap-2">
                <Brain size={16} />
                <span>
                  {model.name} ({model.architecture})
                </span>
              </div>

              {isSelected && (
                <span className="w-2 h-2 bg-green-400 rounded-full" />
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default ModelList;