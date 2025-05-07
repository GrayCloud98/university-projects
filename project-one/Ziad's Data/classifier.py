import pandas as pd
import glob
from sklearn.ensemble import RandomForestClassifier
import joblib

# === Configurable Gesture Names ===
gestures = ['Rock', 'Paper', 'Scissors']

# === Load Data ===
X = []
y = []

print("Loading data...")

for gesture in gestures:
    csv_files = glob.glob(f"{gesture}/*.csv")
    for file_path in csv_files:
        print(f"Processing {file_path}...")
        df = pd.read_csv(file_path, sep=';')

        # Extract features: mean and std for each axis
        features = [
            df['accX'].mean(), df['accX'].std(),
            df['accY'].mean(), df['accY'].std(),
            df['accZ'].mean(), df['accZ'].std(),
            df['gyroX'].mean(), df['gyroX'].std(),
            df['gyroY'].mean(), df['gyroY'].std(),
            df['gyroZ'].mean(), df['gyroZ'].std()
        ]

        X.append(features)
        y.append(gesture)

print("Training model...")

# === Train the Model ===
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X, y)

# === Save the Model ===
joblib.dump(clf, 'gesture_model.pkl')
print("Model trained and saved as gesture_model.pkl")
