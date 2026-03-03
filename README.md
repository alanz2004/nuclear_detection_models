# Nuclear AI Safety Detection

AI system for **early nuclear reactor accident detection** using deep learning on reactor telemetry data.

This project combines:

- 🧠 **LSTM deep learning models**
- ⚡ **FastAPI ML inference server**
- 📊 **React monitoring dashboard**

to detect **early accident signals** in nuclear reactor telemetry.

---

## Problem

Early detection of nuclear reactor incidents is critical for **reactor safety and damage prevention**.

Traditional monitoring systems rely on **static threshold alerts**, which often fail to detect:

- complex temporal relationships
- early anomaly signals
- multi-variable interactions

This can delay detection of dangerous events such as:

- **LOCA — Loss of Coolant Accident**
- **LOF — Loss of Flow**
- abnormal thermal conditions

---

## Solution

This system trains **deep learning time-series models (LSTM)** on reactor telemetry data to detect accident patterns.

The system architecture allows:

- AI accident detection
- model performance monitoring
- simulation testing
- visualization of model metadata

---

## System Architecture

![Architecture](docs/architecture.png)

Pipeline:
# Nuclear AI Safety Detection

AI system for **early nuclear reactor accident detection** using deep learning on reactor telemetry data.

This project combines:

- 🧠 **LSTM deep learning models**
- ⚡ **FastAPI ML inference server**
- 📊 **React monitoring dashboard**

to detect **early accident signals** in nuclear reactor telemetry.

---

## Problem

Early detection of nuclear reactor incidents is critical for **reactor safety and damage prevention**.

Traditional monitoring systems rely on **static threshold alerts**, which often fail to detect:

- complex temporal relationships
- early anomaly signals
- multi-variable interactions

This can delay detection of dangerous events such as:

- **LOCA — Loss of Coolant Accident**
- **LOF — Loss of Flow**
- abnormal thermal conditions

---

## Solution

This system trains **deep learning time-series models (LSTM)** on reactor telemetry data to detect accident patterns.

The system architecture allows:

- AI accident detection
- model performance monitoring
- simulation testing
- visualization of model metadata

---

## System Architecture

![Architecture](docs/architecture.png)

Pipeline:

React Dashboard
│
▼
FastAPI ML Server
│
▼
TensorFlow LSTM Model
│
▼
Reactor Telemetry Data


---

## Features

- LSTM accident detection model
- FastAPI ML server
- React monitoring dashboard
- Model metadata API
- Simulation testing interface
- JSON-based model registry
- Confusion matrix visualization
- Dataset statistics visualization

---

## Repository Structure

---

## Features

- LSTM accident detection model
- FastAPI ML server
- React monitoring dashboard
- Model metadata API
- Simulation testing interface
- JSON-based model registry
- Confusion matrix visualization
- Dataset statistics visualization

---

## Repository Structure
project-root
│
├── server
│   ├── app
│   │   ├── api
│   │   │   └── models.py
│   │   │
│   │   ├── services
│   │   │   └── model_manager.py
│   │   │
│   │   └── core
│   │
│   ├── models
│   │   ├── LSTM_LOCA_Model_info.json
│   │   └── final_model.keras
│   │
│   ├── main.py
│   └── requirements.txt
│
├── frontend
│   └── neural-sight-dashboard
│
├── NuclearPowerPlantAccidentData
│   ├── datasets
│   └── scripts
│
└── docs
    └── architecture.png

# Backend Installation (FastAPI)

## 1 Clone repository

```bash
git clone https://github.com/YOUR_USERNAME/nuclear-ai-safety-detection.git
cd nuclear-ai-safety-detection

## Backend Installation (FastAPI)

### 1 Navigate to server folder

```bash
cd server
```

### 2 Create virtual environment

```bash
python -m venv venv
```

Activate it.

#### Windows

```bash
venv\Scripts\activate
```

#### Mac/Linux

```bash
source venv/bin/activate
```

### 3 Install dependencies

```bash
pip install -r requirements.txt
```

Example `requirements.txt`

```
fastapi
uvicorn
tensorflow
numpy
scikit-learn
joblib
```

### 4 Start the FastAPI server

```bash
uvicorn main:app --reload
```

Server will run at

```
http://localhost:8000
```

API documentation

```
http://localhost:8000/docs
```

---

# Frontend Installation (React Dashboard)

### 1 Navigate to frontend folder

```bash
cd frontend
```

### 2 Install dependencies

```bash
npm install
```

### 3 Start frontend

```bash
npm run dev
```

Frontend runs at

```
http://localhost:5173
```

---

# API Endpoints

## Get All Models

```
GET /models/all/info
```

Returns metadata for all trained models.

---

## Example API Response

```json
[
  {
    "id": "1513a28c-1438-43d0-bfdf-44d1ed5d12ed",
    "name": "LSTM_LOCA_Model",
    "architecture": "LSTM with Dropout",
    "version": "1.0",
    "accuracy": 0.9962,
    "validation": 0.9940,
    "precision": 1.0,
    "confusionMatrix": [
      [205, 0],
      [2, 332]
    ],
    "description": "HIGH-LEVEL AI - Excellent detection performance",
    "dropoutRate": 0.4,
    "learningRate": 0.00005,
    "dataset": {
      "totalSize": 2694,
      "features": [
        "PWR",
        "TAVG",
        "TF",
        "TFPK",
        "DNBR",
        "VOID"
      ],
      "source": "LOCA sliding window dataset",
      "accidentPercentage": 61.99
    }
  }
]
```

---

# Technologies Used

## Backend

- Python
- FastAPI
- TensorFlow
- NumPy
- Scikit-learn

## Frontend

- React
- TypeScript
- Axios
- TailwindCSS

---

# Model Details

## Model type

```
LSTM (Long Short-Term Memory)
```

## Input

```
60 time steps
14 reactor telemetry features
```

## Output

```
Binary classification
Normal / Accident
```

---

# Example Model Performance

```
Accuracy : 0.9998
Precision: 0.9996
Recall   : 1.0000
F1 Score : 0.9998
ROC AUC  : 1.0000
```

## Confusion Matrix

```
[[2754    1]
 [   0 2448]]
```

---

# Author

Alan Starobinski  
AI / Full Stack Developer

---

# License

MIT License