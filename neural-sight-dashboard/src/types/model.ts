export interface Dataset {
  totalSize: number;      // total number of samples
  features: string[];     // list of feature names
  source: string;         // dataset source or description
  accidentPercentage: number;
}

export interface Model {
  id: string;
  name: string;
  architecture: string;
  version: string;
  accuracy: number;       // 0 - 1
  validation: number;     // 0 - 1
  precision: number;      // 0 - 1
  confusionMatrix: number[][]; // [[TP, FP],[FN, TN]] or your preferred format
  description: string;
  dropoutRate: number;
  learningRate: number;
  dataset: Dataset;       // updated type
}