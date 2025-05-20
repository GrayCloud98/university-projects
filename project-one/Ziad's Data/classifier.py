import pandas as pd
import glob
from sklearn.ensemble import RandomForestClassifier
import joblib

# === Configurable Person Names and Gestures ===
persons = ['Z', 'K']
gestures = ['Rock', 'Paper', 'Scissors']

# === Load Data ===
X = []
y = []

print("🔄 Loading and processing data...")

for person in persons:
    for gesture in gestures:
        csv_files = glob.glob(
            f"C:/Users/Ziad Morsy/PycharmProjects/group-c/project-one/Ziad's Data/{person}/{gesture}/*_cleaned.csv")

        for file_path in csv_files:
            print(f"Processing {file_path}...")

            # Read the cleaned CSV
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

            # Append to training data
            X.append(features)
            y.append(gesture)

print("✅ Data loaded and processed.")

# === Train the Model ===
print("🔄 Training the RandomForest model...")
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X, y)

# === Save the Model ===
model_path = "gesture_model.pkl"
joblib.dump(clf, model_path)
print(f"✅ Model trained and saved as {model_path}")
