# ============================================================
# File: generate_combined_LOCA_balanced_fixed.py
# Purpose: Fixed version - No label leakage + realistic augmentation
# ============================================================

import os
import pandas as pd
import numpy as np

# ==============================
# Configuration
# ==============================
NORMAL_FOLDER = "../Operation_csv_data/Normal"
LOCA_FOLDER = "../Operation_csv_data/LOCA"
OUTPUT_FOLDER = "../Data_Sets_csv/Dataset_LOCA"

TIME_STEP = 1                    # seconds
ACCIDENT_THRESHOLD = 3           # std multiplier to detect accident start
ACCIDENT_LABEL_DELAY = 30        # <<< IMPORTANT: seconds after accident start before labeling as LOCA (prevents leakage)
NOISE_LEVEL = 0.01               # 1% relative noise for augmentation (realistic)

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ==============================
# Features
# ==============================
FEATURES = [
    "PWR", "TAVG", "TF", "TFPK", "DNBR", "VOID",
    "WRCA", "WRCB", "P", "PPM"
]

DERIV_COLS = ["PWR", "TAVG", "TF", "DNBR", "WRCA", "WRCB"]

all_dfs = []

# ==============================
# Helper: detect accident start
# ==============================
def detect_accident_start(df, column="WRCA", threshold_multiplier=ACCIDENT_THRESHOLD):
    """Return first index where sudden change is detected."""
    if column not in df.columns:
        return None
    diff = df[column].diff().abs()
    threshold = diff.mean() + threshold_multiplier * diff.std()
    accident_idx = diff[diff > threshold].index
    return accident_idx[0] if len(accident_idx) > 0 else None

# ==============================
# Process NORMAL dataset
# ==============================
print("Processing NORMAL data...")

normal_dfs = []

for file in os.listdir(NORMAL_FOLDER):
    if not file.endswith(".csv"):
        continue
    path = os.path.join(NORMAL_FOLDER, file)
    df = pd.read_csv(path).sort_values("TIME").reset_index(drop=True)

    available_features = [f for f in FEATURES if f in df.columns]
    df = df[["TIME"] + available_features]

    # Interpolation to uniform timestep
    new_time = np.arange(df["TIME"].min(), df["TIME"].max() + TIME_STEP, TIME_STEP)
    df_interp = pd.DataFrame({"TIME": new_time})
    for col in available_features:
        df_interp[col] = np.interp(new_time, df["TIME"], df[col])

    # Derivatives
    for col in DERIV_COLS:
        if col in df_interp.columns:
            df_interp[f"d{col}"] = df_interp[col].diff().fillna(0)

    df_interp["LOCA_label"] = 0
    normal_dfs.append(df_interp)

df_normal_all = pd.concat(normal_dfs, ignore_index=True)
n_normal = len(df_normal_all)
print(f"Total normal samples: {n_normal}")

# ==============================
# Process LOCA accident dataset
# ==============================
print("\nProcessing LOCA accident data...")

loca_dfs = []

for file in os.listdir(LOCA_FOLDER):
    if not file.endswith(".csv"):
        continue
    path = os.path.join(LOCA_FOLDER, file)
    df = pd.read_csv(path).sort_values("TIME").reset_index(drop=True)

    available_features = [f for f in FEATURES if f in df.columns]
    df = df[["TIME"] + available_features]

    # Interpolation
    new_time = np.arange(df["TIME"].min(), df["TIME"].max() + TIME_STEP, TIME_STEP)
    df_interp = pd.DataFrame({"TIME": new_time})
    for col in available_features:
        df_interp[col] = np.interp(new_time, df["TIME"], df[col])

    # Derivatives
    for col in DERIV_COLS:
        if col in df_interp.columns:
            df_interp[f"d{col}"] = df_interp[col].diff().fillna(0)

    # === FIXED LABELING - No future leakage ===
    accident_start = detect_accident_start(df_interp, column="WRCA")
    if accident_start is None:
        print(f"Warning: No accident detected in {file} → labeling all as normal")
        df_interp["LOCA_label"] = 0
    else:
        df_interp["LOCA_label"] = 0
        start_label_idx = accident_start + ACCIDENT_LABEL_DELAY
        if start_label_idx < len(df_interp):
            df_interp.loc[start_label_idx:, "LOCA_label"] = 1
            print(f"✓ Accident detected in {file} at index {accident_start} → labeling starts at {start_label_idx}")
        else:
            print(f"Warning: Accident too close to end in {file}")

    loca_dfs.append(df_interp)

df_loca_all = pd.concat(loca_dfs, ignore_index=True)
n_loca = len(df_loca_all)
print(f"Total LOCA samples: {n_loca}")

# ==============================
# Augment Normal rows to balance
# ==============================
needed_multiplier = int(np.ceil(n_loca / n_normal))
print(f"\nNormal augmentation multiplier: {needed_multiplier} (1% relative noise)")

augmented_normals = []
for _ in range(needed_multiplier):
    for df in normal_dfs:
        df_aug = df.copy()
        for col in FEATURES:
            if col in df_aug.columns and df_aug[col].std() > 0:
                # Relative noise (much more realistic)
                df_aug[col] += np.random.normal(0, NOISE_LEVEL * df_aug[col].abs().mean(), size=len(df_aug))
        augmented_normals.append(df_aug)

# ==============================
# Combine everything
# ==============================
all_dfs = augmented_normals + [df_loca_all]
df_combined = pd.concat(all_dfs, ignore_index=True)

# ==============================
# Summary
# ==============================
n_positive = df_combined["LOCA_label"].sum()
n_negative = len(df_combined) - n_positive
positive_ratio = n_positive / len(df_combined)

print("\n===== FINAL DATASET SUMMARY =====")
print(f"Total samples          : {len(df_combined):,}")
print(f"Normal  (label 0)      : {n_negative:,}")
print(f"LOCA    (label 1)      : {n_positive:,}")
print(f"Positive ratio         : {positive_ratio:.4f}")
print(f"Balanced?              : {'Yes' if 0.45 <= positive_ratio <= 0.55 else 'No'}")
print(f"Label delay used       : {ACCIDENT_LABEL_DELAY} seconds (anti-leakage)")

# ==============================
# Save
# ==============================
combined_path = os.path.join(OUTPUT_FOLDER, "LOCA_dataset_combined_fixed.csv")
df_combined.to_csv(combined_path, index=False)
print(f"\n✅ Fixed dataset saved to: {combined_path}")