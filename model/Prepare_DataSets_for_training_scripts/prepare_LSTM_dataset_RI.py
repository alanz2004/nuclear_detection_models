# =====================================================
# File: prepare_lstm_dataset_ri.py
# Purpose: Prepare sliding window dataset for LSTM with oversampling for RI dataset
# RI: Uses Dataset_RI folder, includes class balance check, feature scaling, windowing
# =====================================================

import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler
import joblib

# ==============================
# Configuration
# ==============================

INPUT_PATH = "../Data_Sets_csv/Dataset_RI/RI_dataset_combined.csv"  # RI: your combined RI dataset
OUTPUT_FOLDER = "../Data_Sets_training/LSTM_Dataset_RI"
WINDOW_SIZE = 50   # RI: default LSTM window size (can experiment)
STEP_SIZE = 5      # RI: sliding window step
LABEL_COLUMN = "RI_label"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ==============================
# Load Data
# ==============================

print("Loading RI dataset...")
df = pd.read_csv(INPUT_PATH)

# ------------------------------
# Separate features and label
# ------------------------------

features = df.drop(columns=[LABEL_COLUMN])
labels = df[LABEL_COLUMN]

# ------------------------------
# Check class balance
# ------------------------------

print("Class distribution (RI):")
print(labels.value_counts())
print("Positive ratio (RI):", labels.mean())

# ==============================
# Normalize Features
# ==============================

scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)
joblib.dump(scaler, os.path.join(OUTPUT_FOLDER, "scaler.pkl"))
print("Scaler saved (RI).")

# ==============================
# Create Sliding Windows
# ==============================

X = []
y = []

for i in range(0, len(features_scaled) - WINDOW_SIZE, STEP_SIZE):
    window = features_scaled[i:i+WINDOW_SIZE]
    # RI: window label is 1 if any timestep in the window is positive
    label = int(labels.iloc[i:i+WINDOW_SIZE].any())
    X.append(window)
    y.append(label)

X = np.array(X)
y = np.array(y)

print("Windowed dataset shape (RI):", X.shape)
print("Positive samples after windows (RI):", np.sum(y))

# ==============================
# Oversample Minority Class
# ==============================

# Flatten windows for oversampling
X_flat = X.reshape(len(X), -1)

ros = RandomOverSampler(random_state=42)
X_resampled, y_resampled = ros.fit_resample(X_flat, y)

# Reshape back to original sliding window shape
X_resampled = X_resampled.reshape(-1, WINDOW_SIZE, X.shape[2])
y_resampled = y_resampled

print("Positive samples after oversampling (RI):", np.sum(y_resampled))
print("Total samples after oversampling (RI):", len(y_resampled))

# ==============================
# Shuffle Data
# ==============================

indices = np.arange(len(X_resampled))
np.random.seed(42)
np.random.shuffle(indices)
X_resampled = X_resampled[indices]
y_resampled = y_resampled[indices]

# ==============================
# Train/Test Split
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled,
    test_size=0.2,
    stratify=y_resampled,
    random_state=42
)

# ==============================
# Save Arrays
# ==============================

np.save(os.path.join(OUTPUT_FOLDER, "X_train.npy"), X_train)
np.save(os.path.join(OUTPUT_FOLDER, "X_test.npy"), X_test)
np.save(os.path.join(OUTPUT_FOLDER, "y_train.npy"), y_train)
np.save(os.path.join(OUTPUT_FOLDER, "y_test.npy"), y_test)

print("RI dataset ready for LSTM.")
print("Training shape:", X_train.shape, "Test shape:", X_test.shape)
print("Positive ratio in training (RI):", np.mean(y_train))