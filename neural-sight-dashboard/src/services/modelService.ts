import api from "./api";
import type { Model } from "../types/model";

// Fetch model metrics from backend
export const getModelMetrics = async () => {
  const res = await api.get("/models/metrics");
  return res.data;
};

// Run a simulation
export const runSimulation = async (data: any) => {
  const res = await api.post("/models/simulate", data);
  return res.data;
};

// Return mock models with proper Dataset structure
// Fetch all models info from backend
export const getModels = async (): Promise<Model[]> => {
  try {
    const res = await api.get("/models/all/info"); // endpoint that returns all JSON infos
    return res.data.models_info; // adjust if your backend wraps it differently
  } catch (error) {
    console.error("Failed to fetch models:", error);
    return [];
  }
};