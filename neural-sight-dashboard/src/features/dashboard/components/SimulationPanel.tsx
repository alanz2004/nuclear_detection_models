import { Play } from "lucide-react";

export const SimulationPanel = () => {
  return (
    <div className="bg-gray-900 p-3 rounded-lg w-full md:w-1/3 flex flex-col border border-blue-500 h-72">
      {/* Panel Title with Icon */}
      <div className="flex items-center gap-2 mb-2">
        <Play size={18} className="text-blue-500" />
        <h3 className="text-white font-semibold text-lg">Simulation Lab</h3>
      </div>

      {/* Streamer + Button container */}
      <div className="flex flex-col flex-1 justify-between">
        {/* Input Stream / Streamer */}
        <div className="bg-black flex-1 rounded flex items-center justify-center text-gray-500 text-sm">
          Awaiting Input Stream
        </div>

        {/* Run Simulation Button */}
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded w-full mt-4">
          Run Simulation
        </button>
      </div>
    </div>
  );
};