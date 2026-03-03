import { useModel } from "../../../context/ModelContext";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Activity } from "lucide-react";

// Register the required Chart.js components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export const TrainingGraph = () => {
  const { selectedModel } = useModel();
  if (!selectedModel) return null;

  // For mock purposes, if selectedModel.accuracy and validation are numbers, we need arrays
  const trainingData = Array(50).fill(selectedModel.accuracy);
  const validationData = Array(50).fill(selectedModel.validation);

  const data = {
    labels: Array.from({ length: 50 }, (_, i) => `Epoch ${i + 1}`),
    datasets: [
      {
        label: "Training Accuracy",
        data: trainingData,
        borderColor: "#3B82F6",
        fill: false,
        tension: 0.3,
      },
      {
        label: "Validation Accuracy",
        data: validationData,
        borderColor: "#A78BFA",
        fill: false,
        tension: 0.3,
      },
    ],
  };

  return (
    <div className="bg-gray-900 p-4 rounded-lg w-full flex flex-col gap-4">
      {/* Chart Title with Icon */}
      <div className="flex items-center gap-2">
        <Activity size={20} className="text-blue-500" />
        <h3 className="text-white font-semibold text-lg">
          Training with Validation Accuracy
        </h3>
      </div>

      {/* Chart */}
      <Line data={data} />
    </div>
  );
};