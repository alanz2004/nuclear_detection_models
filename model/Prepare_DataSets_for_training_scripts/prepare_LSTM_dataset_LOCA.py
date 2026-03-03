# =====================================================
# File: prepare_lstm_dataset_looca_shuffled_only.py
# Purpose: Prepare sliding window dataset for LSTM/CNN
# FIXED:
#   - Uses pre-balanced dataset
#   - No oversampling
#   - Sliding window uses last timestep label
#   - Prints Normal/LOCA counts
#   - Shuffles training windows
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

INPUT_PATH = "../Data_Sets_csv/Dataset_LOCA/LOCA_dataset_combined.csv"
OUTPUT_FOLDER = "../Data_Sets_training/LSTM_Dataset_LOCA"

WINDOW_SIZE = 60   # timesteps per sample
STEP_SIZE = 30     # sliding window step

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ==============================
# Load Data
# ==============================

print("Loading combined LOCA + Normal dataset...")
df = pd.read_csv(INPUT_PATH)
print("Dataset shape:", df.shape)

# Drop TIME column if present
if "TIME" in df.columns:
    df = df.drop(columns=["TIME"])
    print("TIME column removed.")

# ==============================
# Features & Labels
# ==============================

loca_features = [
    "PWR","TAVG","TF","TFPK","DNBR","VOID",
    "WRCA","WRCB","P","PPM",
    "dPWR","dTAVG","dTF","dDNBR"
]

features = df[loca_features]
labels = df["LOCA_label"]

print("\nFeature columns used for training:", loca_features)
print("Original positive ratio:", labels.mean())

# ==============================
# Normalize Features
# ==============================

print("\nNormalizing features...")
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)
joblib.dump(scaler, os.path.join(OUTPUT_FOLDER, "scaler.pkl"))
print("Scaler saved.")

# ==============================
# Train/Test Split
# ==============================

print("\nSplitting dataset (80/20 train/test)...")
X_train_full, X_test_full, y_train_full, y_test_full = train_test_split(
    features_scaled,
    labels.values,
    test_size=0.2,
    stratify=labels,
    random_state=42
)

print("Training set shape:", X_train_full.shape)
print("Testing set shape:", X_test_full.shape)
print("Training positive ratio:", y_train_full.mean())
print("Testing positive ratio:", y_test_full.mean())

# ==============================
# Sliding Windows Function
# ==============================

def create_sliding_windows(X, y, window_size=WINDOW_SIZE, step_size=STEP_SIZE, shuffle=False):
    X_windows = []
    y_windows = []

    for i in range(0, len(X) - window_size, step_size):
        window = X[i:i+window_size]
        label = y[i + window_size - 1]  # last timestep label
        X_windows.append(window)
        y_windows.append(label)

    X_windows = np.array(X_windows)
    y_windows = np.array(y_windows)
    
    # Shuffle if needed
    if shuffle:
        idx = np.random.permutation(len(X_windows))
        X_windows = X_windows[idx]
        y_windows = y_windows[idx]
    
    # Print counts
    n_positive = np.sum(y_windows)
    n_negative = len(y_windows) - n_positive
    print(f"Sliding windows: Total={len(y_windows)}, Normal={n_negative}, LOCA={n_positive}, Positive ratio={n_positive/len(y_windows):.4f}")
    
    return X_windows, y_windows

# ==============================
# Create Sliding Windows
# ==============================

print("\nCreating sliding windows for training set...")
X_train, y_train = create_sliding_windows(X_train_full, y_train_full, shuffle=True)
print("Training windowed dataset shape:", X_train.shape)

print("\nCreating sliding windows for test set...")
X_test, y_test = create_sliding_windows(X_test_full, y_test_full, shuffle=False)
print("Test windowed dataset shape:", X_test.shape)

# ==============================
# Save Arrays
# ==============================

np.save(os.path.join(OUTPUT_FOLDER, "X_train.npy"), X_train)
np.save(os.path.join(OUTPUT_FOLDER, "X_test.npy"), X_test)
np.save(os.path.join(OUTPUT_FOLDER, "y_train.npy"), y_train)
np.save(os.path.join(OUTPUT_FOLDER, "y_test.npy"), y_test)

# ==============================
# Final Summary
# ==============================

print("\n========== LOCA LSTM DATASET READY ==========")
print("Training shape:", X_train.shape)
print("Test shape:", X_test.shape)
print("\nTraining positive ratio:", y_train.mean())
print("Testing positive ratio:", y_test.mean())
print("\nEach sample shape:")
print("timesteps =", X_train.shape[1])
print("features =", X_train.shape[2])