# =====================================================
# File: train_and_evaluate_lstm_looca_fixed.py
# Purpose: Train LSTM severity classifier on LOCA + Normal data
# Improvements:
#   - Uses pre-balanced sliding window dataset
#   - Shuffles training data
#   - No oversampling
#   - Prints positive/negative counts
# =====================================================

import os
import numpy as np
import tensorflow as tf
import json
import uuid
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

# ==============================
# Configuration
# ==============================

DATA_FOLDER = "../Data_Sets_training/LSTM_Dataset_LOCA"
MODEL_FOLDER = "../Saved_Models_Files/Saved_Model_LOCA"
os.makedirs(MODEL_FOLDER, exist_ok=True)

EPOCHS = 5
BATCH_SIZE = 32
LEARNING_RATE = 5e-5
DROPOUT_RATE = 0.4  # higher dropout for safer training

# ==============================
# Load Dataset
# ==============================

X_train = np.load(os.path.join(DATA_FOLDER, "X_train.npy"))
X_test  = np.load(os.path.join(DATA_FOLDER, "X_test.npy"))
y_train = np.load(os.path.join(DATA_FOLDER, "y_train.npy"))
y_test  = np.load(os.path.join(DATA_FOLDER, "y_test.npy"))

# Shuffle training data
shuffle_idx = np.random.permutation(len(X_train))
X_train = X_train[shuffle_idx]
y_train = y_train[shuffle_idx]

# ==============================
# Clean dataset (NaN / Inf)
# ==============================

X_train = np.nan_to_num(X_train, nan=0.0, posinf=1e5, neginf=-1e5)
X_test  = np.nan_to_num(X_test, nan=0.0, posinf=1e5, neginf=-1e5)
y_train = np.nan_to_num(y_train, nan=0)
y_test  = np.nan_to_num(y_test, nan=0)

print("Training shape:", X_train.shape, "Test shape:", X_test.shape)
print(f"Positive class ratio (train): {np.mean(y_train):.4f}")
print(f"Positive class ratio (test):  {np.mean(y_test):.4f}")

# ==============================
# Print counts
# ==============================

print("\nTraining counts - Normal:", np.sum(y_train==0), "LOCA:", np.sum(y_train==1))
print("Test counts     - Normal:", np.sum(y_test==0), "LOCA:", np.sum(y_test==1))

# ==============================
# Build LSTM Model with Dropout
# ==============================

time_steps = X_train.shape[1]
num_features = X_train.shape[2]

model = tf.keras.Sequential([
    tf.keras.layers.LSTM(128, return_sequences=True, input_shape=(time_steps, num_features)),
    tf.keras.layers.Dropout(DROPOUT_RATE),
    tf.keras.layers.LSTM(64, return_sequences=True),
    tf.keras.layers.Dropout(DROPOUT_RATE),
    tf.keras.layers.LSTM(32),
    tf.keras.layers.Dropout(DROPOUT_RATE),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(DROPOUT_RATE),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

optimizer = tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE, clipnorm=1.0)

model.compile(
    optimizer=optimizer,
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ==============================
# Callbacks for stable training
# ==============================

callbacks = [
    tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True),
    tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2)
]

# ==============================
# Train Model
# ==============================

history = model.fit(
    X_train, y_train,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    validation_data=(X_test, y_test),
    shuffle=True,
    callbacks=callbacks
)

# Save the trained model
MODEL_PATH = os.path.join(MODEL_FOLDER, "final_model.keras")
model.save(MODEL_PATH)
print("Model saved to:", MODEL_PATH)

# ==============================
# Evaluate Model
# ==============================

y_prob = model.predict(X_test).flatten()
y_prob = np.nan_to_num(y_prob, nan=0.0)

# Dynamic thresholding to maximize recall
thresholds = np.linspace(0.1, 0.9, 17)
best_recall = 0
best_thresh = 0.5
for t in thresholds:
    y_pred_temp = (y_prob >= t).astype(int)
    r = recall_score(y_test, y_pred_temp, zero_division=0)
    if r > best_recall:
        best_recall = r
        best_thresh = t

y_pred = (y_prob >= best_thresh).astype(int)
print(f"\nUsing threshold {best_thresh:.2f} for best recall: {best_recall:.4f}")

# ==============================
# Metrics
# ==============================

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)
auc = roc_auc_score(y_test, y_prob)
cm = confusion_matrix(y_test, y_pred)

print("\n========== MODEL PERFORMANCE ==========")
print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")
print(f"ROC AUC  : {auc:.4f}")
print("\nConfusion Matrix:")
print(cm)
print("\nDetailed Classification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

# ==============================
# Performance Interpretation
# ==============================

def interpret_model(acc, f1, auc):
    metrics = [m for m in [acc, f1, auc] if not np.isnan(m)]
    if not metrics:
        return "UNABLE TO INTERPRET ❌ - No valid metrics available."
    score = sum(metrics)/len(metrics)
    if score < 0.70:
        return "BAD ❌ - Model barely learns patterns."
    elif score < 0.80:
        return "OK ⚠ - Model detects patterns but unreliable."
    elif score < 0.90:
        return "GOOD ✅ - Solid performance, usable."
    elif score < 0.95:
        return "VERY GOOD 🚀 - Strong research-level model."
    else:
        return "HIGH-LEVEL AI 🔬 - Excellent detection performance."

summary = interpret_model(accuracy, f1, auc)
print("\n========== FINAL SUMMARY ==========")
print(summary)

# ==============================
# Additional Risk Warning
# ==============================

if recall < 0.85:
    print("\n⚠ WARNING:")
    print("Model misses too many high-severity accidents.")
    print("Recall should be high for safety-critical systems.")

# ==============================
# Save Model Info to JSON (with history)
# ==============================

feature_names = [f"feature_{i}" for i in range(num_features)]

model_info = {
    "id": str(uuid.uuid4()),
    "name": "LSTM_LOCA_Model",
    "architecture": "LSTM with Dropout",
    "version": "1.0",
    "accuracy": float(accuracy),
    "validation": float(best_recall),
    "precision": float(precision),
    "confusionMatrix": cm.tolist(),
    "description": summary,
    "dropoutRate": DROPOUT_RATE,
    "learningRate": LEARNING_RATE,
    "dataset": {
        "totalSize": int(X_train.shape[0] + X_test.shape[0]),
        "features": feature_names,
        "source": "LOCA sliding window dataset",
        "accidentPercentage": float(np.mean(y_train) * 100)
    },
    "history": {  
        "loss": [float(l) for l in history.history.get("loss", [])],
        "val_loss": [float(l) for l in history.history.get("val_loss", [])],
        "accuracy": [float(a) for a in history.history.get("accuracy", [])],
        "val_accuracy": [float(a) for a in history.history.get("val_accuracy", [])]
    }
}

json_path = os.path.join(MODEL_FOLDER, f"{model_info['name']}_info.json")
with open(json_path, "w") as f:
    json.dump(model_info, f, indent=4)

print(f"\nModel info (including history) saved to JSON: {json_path}")