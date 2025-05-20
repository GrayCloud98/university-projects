import pandas as pd
import glob
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# === Configurable Gestures ===
gestures = ['Rock', 'Paper', 'Scissors']

# === Load Data ===
X = []
y = []

print("🔄 Loading and processing data...")

for gesture in gestures:
    csv_files = glob.glob(
        f"C:/Users/Ziad Morsy/PycharmProjects/group-c/project-one/Ziad's Data/Cleaned/{gesture}/*_cleaned.csv")

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

        X.append(features)
        y.append(gesture)

print("✅ Data loaded and processed.")

# === Split Data ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, stratify=y, random_state=42)

# === Train the Model ===
print("🔄 Training the RandomForest model...")
clf = RandomForestClassifier(n_estimators=80, random_state=42)
clf.fit(X_train, y_train)

# === Evaluation ===
y_pred = clf.predict(X_test)

cm = confusion_matrix(y_test, y_pred, labels=gestures)
print("\n🔍 Confusion Matrix:")
print(cm)

print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred, target_names=gestures))

plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', xticklabels=gestures, yticklabels=gestures, cmap="Blues")
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.tight_layout()
plt.show()

print("\n✅ Train Accuracy:", clf.score(X_train, y_train))
print("✅ Test Accuracy:", clf.score(X_test, y_test))

# === Save the Model ===
model_path = "gesture_model.pkl"
joblib.dump(clf, model_path)
print(f"✅ Model trained and saved as {model_path}")
