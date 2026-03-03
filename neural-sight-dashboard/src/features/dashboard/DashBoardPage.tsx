import {
  MetricCard,
  TrainingGraph,
  SimulationPanel,
  ConfusionMatrix,
  ModelDescription,
  DatasetMetadata
} from "./components/index";

const DashboardPage = () => {
  return (
    <div className="p-6 grid gap-6">
      {/* Page Titles */}
      <div className="flex flex-col gap-2 mb-6">
        <h1 className="text-3xl md:text-4xl font-bold text-white">Model Performance Overview</h1>

        {/* Subtitle + GPU Status */}
        <div className="flex items-center justify-between">
          <h2 className="text-sm md:text-base text-gray-400">
            Real-time analysis and architecture validation for{" "}
            <span className="text-blue-500 font-semibold">LSTM</span>
          </h2>

          {/* GPU Status */}
          <div className="flex items-center gap-2 bg-gray-800 px-3 py-1 rounded-full shadow-sm">
            <span className="w-2 h-2 bg-green-400 rounded-full" />
            <span className="text-xs md:text-sm text-white font-medium">GPU Status: Optimal</span>
          </div>
        </div>
      </div>

      {/* Top metrics */}
      <div className="flex flex-col md:flex-row gap-6">
        <MetricCard type="accuracy" delta={2.1} />
        <MetricCard type="precision" delta={-0.5} />
        <MetricCard type="recall" delta={1.7} />
      </div>

      {/* Training graph + simulation panel */}
      <div className="flex flex-col md:flex-row gap-6">
        <TrainingGraph />
        <SimulationPanel />
      </div>

      {/* Confusion matrix + model description */}
      <div className="flex flex-col md:flex-row gap-6">
        <ConfusionMatrix />
        <ModelDescription />
        <DatasetMetadata />
      </div>
    </div>
  );
};

export default DashboardPage;