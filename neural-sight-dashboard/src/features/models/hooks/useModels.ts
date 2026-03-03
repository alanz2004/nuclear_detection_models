import { useEffect, useState } from "react";
import { getModels } from "../../../services/modelService";
import type { Model } from "../../../types/model";

export const useModels = () => {
  const [models, setModels] = useState<Model[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchModels = async () => {
      try {
        setLoading(true);

        const data = await getModels();

        setModels(data);
      } catch (err) {
        setError("Failed to load models");
      } finally {
        setLoading(false);
      }
    };

    fetchModels();
  }, []);

  return { models, loading, error };
};
