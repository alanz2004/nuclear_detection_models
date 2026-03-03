import os
import pandas as pd
import numpy as np

# ==============================
# Configuration
# ==============================
NORMAL_FOLDER = "../Operation_csv_data/Normal"
LOF_FOLDER = "../Operation_csv_data/LOF"
OUTPUT_FOLDER = "../Data_Sets_csv/Dataset_LOF"

TIME_STEP = 1
ACCIDENT_START_TIME = 100

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ==============================
# Selected LOF Features
# ==============================
features = [
    "WRCA","WRCB","WLR","WUP",
    "RRCA","RRCB",
    "TAVG","THA","THB","TCA","TCB",
    "PWR","PWNT",
    "TF","TFPK","TFSB",
    "DNBR","TPCT"
]

all_dfs = []

# ==============================
# NORMAL DATASET
# ==============================
print("Processing NORMAL data...")

for file in os.listdir(NORMAL_FOLDER):
    if file.endswith(".csv"):

        path = os.path.join(NORMAL_FOLDER, file)

        df = pd.read_csv(path).sort_values("TIME").reset_index(drop=True)

        df = df[["TIME"] + features]

        # Interpolate to uniform timestep
        time_start, time_end = df["TIME"].min(), df["TIME"].max()

        new_time = np.arange(time_start, time_end + TIME_STEP, TIME_STEP)

        df_interp = pd.DataFrame({"TIME": new_time})

        for col in features:
            df_interp[col] = np.interp(new_time, df["TIME"], df[col])

        # Derivatives
        df_interp["dPWR"] = df_interp["PWR"].diff().fillna(0)
        df_interp["dTAVG"] = df_interp["TAVG"].diff().fillna(0)
        df_interp["dWRCA"] = df_interp["WRCA"].diff().fillna(0)
        df_interp["dWRCB"] = df_interp["WRCB"].diff().fillna(0)
        df_interp["dDNBR"] = df_interp["DNBR"].diff().fillna(0)

        # Label NORMAL
        df_interp["LOF_label"] = 0

        all_dfs.append(df_interp)


# ==============================
# LOF ACCIDENT DATASET
# ==============================
print("Processing LOF accident data...")

for file in os.listdir(LOF_FOLDER):
    if file.endswith(".csv"):

        path = os.path.join(LOF_FOLDER, file)

        df = pd.read_csv(path).sort_values("TIME").reset_index(drop=True)

        df = df[["TIME"] + features]

        # Interpolation
        time_start, time_end = df["TIME"].min(), df["TIME"].max()

        new_time = np.arange(time_start, time_end + TIME_STEP, TIME_STEP)

        df_interp = pd.DataFrame({"TIME": new_time})

        for col in features:
            df_interp[col] = np.interp(new_time, df["TIME"], df[col])

        # Derivatives
        df_interp["dPWR"] = df_interp["PWR"].diff().fillna(0)
        df_interp["dTAVG"] = df_interp["TAVG"].diff().fillna(0)
        df_interp["dWRCA"] = df_interp["WRCA"].diff().fillna(0)
        df_interp["dWRCB"] = df_interp["WRCB"].diff().fillna(0)
        df_interp["dDNBR"] = df_interp["DNBR"].diff().fillna(0)

        # Label accident AFTER 100 sec
        df_interp["LOF_label"] = (df_interp["TIME"] >= ACCIDENT_START_TIME).astype(int)

        all_dfs.append(df_interp)


# ==============================
# Combine all datasets
# ==============================
print("Combining datasets...")

df_combined = pd.concat(all_dfs, ignore_index=True)

combined_path = os.path.join(OUTPUT_FOLDER, "LOF_dataset_combined.csv")

df_combined.to_csv(combined_path, index=False)


# ==============================
# Summary
# ==============================
print("\nCombined dataset ready for training!")

print("Shape:", df_combined.shape)

print("\nClass distribution:")

print(df_combined["LOF_label"].value_counts())

print("\nPositive ratio:")

print(df_combined["LOF_label"].mean())