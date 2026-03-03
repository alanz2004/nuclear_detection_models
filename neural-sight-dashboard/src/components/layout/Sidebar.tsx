import { FaDatabase, FaFlask, FaSlidersH } from "react-icons/fa"; // import icons
import ModelList from "../../features/models/components/ModelList";

const Sidebar = () => {
  return (
    <div className="w-72 h-screen bg-[#0B1220] border-r border-slate-800 flex flex-col justify-between">

      {/* TOP */}
      <div className="p-6">

        {/* Logo */}
        <div className="flex items-center gap-3 mb-8">
          <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center font-bold">
            AI
          </div>

          <div>
            <p className="font-semibold text-white">NeuralSight</p>
            <p className="text-xs text-gray-400">
              Accident Detection v2.4
            </p>
          </div>
        </div>

        {/* Models */}
        <ModelList />

        {/* Workspace */}
        <div className="mt-10">
          <p className="text-xs text-gray-400 uppercase tracking-wider mb-3">
            Workspace
          </p>

          <div className="flex flex-col gap-2 text-sm">

            <button className="flex items-center gap-2 text-gray-300 hover:bg-slate-700 px-3 py-2 rounded-lg text-left">
              <FaDatabase className="text-gray-400" />
              Datasets
            </button>

            <button className="flex items-center gap-2 text-gray-300 hover:bg-slate-700 px-3 py-2 rounded-lg text-left">
              <FaFlask className="text-gray-400" />
              Simulation Lab
            </button>

            <button className="flex items-center gap-2 text-gray-300 hover:bg-slate-700 px-3 py-2 rounded-lg text-left">
              <FaSlidersH className="text-gray-400" />
              Hyperparameters
            </button>

          </div>
        </div>

      </div>

      {/* Bottom */}
      <div className="p-6">
        <button className="w-full bg-blue-600 hover:bg-blue-700 py-3 rounded-lg text-sm font-medium transition">
          + New Analysis
        </button>
      </div>

    </div>
  )
}

export default Sidebar;
