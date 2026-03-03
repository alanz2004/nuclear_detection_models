# =====================================================
# File: prepare_lstm_dataset_lof.py
# Purpose: Prepare sliding window dataset for LSTM (LOF accident)
# =====================================================

import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib

# ==============================
# Configuration
# ==============================

INPUT_PATH = "../Data_Sets_csv/Dataset_LOF/LOF_dataset_combined.csv"
OUTPUT_FOLDER = "../Data_Sets_training/LSTM_Dataset_LOF"

WINDOW_SIZE = 40   # slightly smaller for smaller dataset
STEP_SIZE = 3

LABEL_COLUMN = "LOF_label"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ==============================
# Load Data
# ==============================

print("Loading LOF dataset...")
df = pd.read_csv(INPUT_PATH)

print("\nDataset shape:", df.shape)

# ==============================
# Remove TIME column
# ==============================

if "TIME" in df.columns:
    df = df.drop(columns=["TIME"])
    print("TIME column removed.")

# ==============================
# Separate features and labels
# ==============================

labels = df[LABEL_COLUMN]
features = df.drop(columns=[LABEL_COLUMN])

print("\nFeature columns used for training:")
print(list(features.columns))

print("\nNumber of features:", features.shape[1])

# ==============================
# Check dataset quality
# ==============================

print("\nChecking for NaN values...")

nan_count = features.isna().sum().sum()

if nan_count > 0:
    print("WARNING: NaN values found:", nan_count)
    features = features.fillna(0)
else:
    print("No NaN values found.")

print("\nChecking class balance:")

print(labels.value_counts())
print("Positive ratio:", labels.mean())

# ==============================
# Normalize Features
# ==============================

print("\nNormalizing features...")

scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

joblib.dump(scaler, os.path.join(OUTPUT_FOLDER, "scaler.pkl"))

print("Scaler saved.")

# ==============================
# Create Sliding Windows
# ==============================

print("\nCreating sliding windows...")

X = []
y = []

for i in range(0, len(features_scaled) - WINDOW_SIZE, STEP_SIZE):

    window = features_scaled[i:i+WINDOW_SIZE]

    # window labeled positive if accident appears inside window
    label = int(labels.iloc[i:i+WINDOW_SIZE].any())

    X.append(window)
    y.append(label)

X = np.array(X)
y = np.array(y)

print("\nWindow dataset shape:", X.shape)

print("Positive samples:", np.sum(y))
print("Negative samples:", len(y) - np.sum(y))

# ==============================
# Shuffle dataset
# ==============================

print("\nShuffling dataset...")

indices = np.arange(len(X))
np.random.seed(42)
np.random.shuffle(indices)

X = X[indices]
y = y[indices]

# ==============================
# Train/Test Split
# ==============================

print("\nCreating train/test split...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

# ==============================
# Save arrays
# ==============================

np.save(os.path.join(OUTPUT_FOLDER, "X_train.npy"), X_train)
np.save(os.path.join(OUTPUT_FOLDER, "X_test.npy"), X_test)

np.save(os.path.join(OUTPUT_FOLDER, "y_train.npy"), y_train)
np.save(os.path.join(OUTPUT_FOLDER, "y_test.npy"), y_test)

# ==============================
# Final summary
# ==============================

print("\n========== LOF LSTM DATASET READY ==========")

print("Training shape:", X_train.shape)
print("Test shape:", X_test.shape)

print("\nPositive ratio in training:", np.mean(y_train))
print("Positive ratio in testing:", np.mean(y_test))

print("\nEach sample shape:")
print("timesteps =", WINDOW_SIZE)
print("features =", X.shape[2])