import os
import pandas as pd
import numpy as np

# ==============================
# Configuration
# ==============================
NORMAL_FOLDER = "../Operation_csv_data/Normal"
RI_FOLDER = "../Operation_csv_data/RI"
OUTPUT_FOLDER = "../Data_Sets_csv/Dataset_RI"
TIME_STEP = 1

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Features for model
features = ["PWR", "TAVG", "TF", "TFPK", "DNBR", "VOID",
            "WRCA", "WRCB", "P", "PPM"]

all_dfs = []

# ==============================
# Process NORMAL dataset
# ==============================
for file in os.listdir(NORMAL_FOLDER):
    if file.endswith(".csv"):
        path = os.path.join(NORMAL_FOLDER, file)
        df = pd.read_csv(path).sort_values("TIME").reset_index(drop=True)
        df = df[["TIME"] + features]

        # Interpolate to uniform time step
        time_start, time_end = df["TIME"].min(), df["TIME"].max()
        new_time = np.arange(time_start, time_end + TIME_STEP, TIME_STEP)
        df_interp = pd.DataFrame({"TIME": new_time})
        for col in features:
            df_interp[col] = np.interp(new_time, df["TIME"], df[col])

        # Compute derivatives
        df_interp["dPWR"] = df_interp["PWR"].diff().fillna(0)
        df_interp["dTAVG"] = df_interp["TAVG"].diff().fillna(0)
        df_interp["dTF"] = df_interp["TF"].diff().fillna(0)
        df_interp["dDNBR"] = df_interp["DNBR"].diff().fillna(0)

        # Label normal
        df_interp["RI_label"] = 0

        all_dfs.append(df_interp)

# ==============================
# Process NEGATIVE RI datasets
# ==============================
for file in os.listdir(RI_FOLDER):
    if file.endswith(".csv"):
        path = os.path.join(RI_FOLDER, file)
        df = pd.read_csv(path).sort_values("TIME").reset_index(drop=True)
        df = df[["TIME"] + features]

        # Interpolate
        time_start, time_end = df["TIME"].min(), df["TIME"].max()
        new_time = np.arange(time_start, time_end + TIME_STEP, TIME_STEP)
        df_interp = pd.DataFrame({"TIME": new_time})
        for col in features:
            df_interp[col] = np.interp(new_time, df["TIME"], df[col])

        # Compute derivatives
        df_interp["dPWR"] = df_interp["PWR"].diff().fillna(0)
        df_interp["dTAVG"] = df_interp["TAVG"].diff().fillna(0)
        df_interp["dTF"] = df_interp["TF"].diff().fillna(0)
        df_interp["dDNBR"] = df_interp["DNBR"].diff().fillna(0)

        # Label negative RI
        df_interp["RI_label"] = 1

        all_dfs.append(df_interp)

# ==============================
# Combine all datasets
# ==============================
df_combined = pd.concat(all_dfs, ignore_index=True)
combined_path = os.path.join(OUTPUT_FOLDER, "RI_dataset_combined.csv")
df_combined.to_csv(combined_path, index=False)

print("Combined dataset ready for training!")
print("Shape:", df_combined.shape)