// MetricCard.tsx
import { useModel } from "../../../context/ModelContext";
import { CheckCircle, Zap, Activity } from "lucide-react";

interface MetricCardProps {
  type: "accuracy" | "precision" | "recall";
  title?: string;       // optional override
  color?: string;       // bar color
  delta?: number;       // optional delta percentage
}

export const MetricCard = ({ type, title, color, delta }: MetricCardProps) => {
  const { selectedModel } = useModel();
  if (!selectedModel) return null;

  // Map metric type to value, default color, default title, and icon
  const metricMap: Record<
    string,
    { value: number; defaultColor: string; defaultTitle: string; Icon: React.FC<any> }
  > = {
    accuracy: {
      value: selectedModel.accuracy,
      defaultColor: "bg-green-500",
      defaultTitle: "Accuracy Score",
      Icon: CheckCircle,
    },
    precision: {
      value: selectedModel.precision,
      defaultColor: "bg-yellow-500",
      defaultTitle: "Precision Score",
      Icon: Zap,
    },
    recall: {
      value: selectedModel.validation,
      defaultColor: "bg-red-500",
      defaultTitle: "Recall Score",
      Icon: Activity,
    },
  };

  const metric = metricMap[type];
  const barColor = color || metric.defaultColor;
  const displayTitle = title || metric.defaultTitle;
  const percentage = (metric.value * 100).toFixed(1);
  const Icon = metric.Icon;

  return (
    <div className="bg-gray-900 p-5 rounded-2xl flex flex-col gap-2 w-full md:w-1/3 shadow-lg hover:scale-105 transform transition duration-200">
      <div className="flex items-center justify-between">
        <span className="text-xs text-gray-400 font-semibold uppercase">{displayTitle}</span>
        <Icon size={16} className="text-gray-400" />
      </div>
      <span className="text-2xl font-bold text-white">{percentage}%</span>
      {delta !== undefined && (
        <span className={`text-sm font-medium ${delta >= 0 ? "text-green-400" : "text-red-400"}`}>
          {delta >= 0 ? "+" : ""}
          {delta}%
        </span>
      )}
      <div className="w-full bg-gray-700 rounded-full h-2 mt-2">
        <div
          className={`${barColor} h-2 rounded-full`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};