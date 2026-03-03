import { createContext, useContext, useState, type FC, type ReactNode } from "react";
import type { Model } from "../types/model";

// 1. Define the shape of the context value
interface ModelContextType {
  selectedModel: Model | null;
  setSelectedModel: (model: Model | null) => void;  // allow null explicitly
}

// 2. Create the context with proper typing + default (never-used) value
const ModelContext = createContext<ModelContextType | undefined>(undefined);

// 3. Provider component
export const ModelProvider: FC<{ children: ReactNode }> = ({ children }) => {
  const [selectedModel, setSelectedModel] = useState<Model | null>(null);

  // Value object – usually no need to memoize here unless you have many consumers
  const value = { selectedModel, setSelectedModel };

  return (
    <ModelContext.Provider value={value}>
      {children}
    </ModelContext.Provider>
  );
};

// 4. Custom hook with type safety and required check
export const useModel = (): ModelContextType => {
  const context = useContext(ModelContext);

  if (context === undefined) {
    throw new Error("useModel must be used within a ModelProvider");
  }

  return context;
};