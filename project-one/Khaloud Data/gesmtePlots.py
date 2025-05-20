import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import numpy as np

# Directory setup
directory = "C:/Users/Admin/PycharmProjects/group-c/project-one/Khaloud Data/TornadoTornado"
csv_files = glob.glob(os.path.join(directory, "recording-*.csv"))

# Initialize storage for all data
all_accX = []

for file_path in csv_files:
    try:
        df = pd.read_csv(file_path, delimiter=';')
        if 'accX' in df.columns:
            # Normalize data to same length (interpolation)
            normalized = np.interp(np.linspace(0, 1, 100),
                                 np.linspace(0, 1, len(df['accX'])),
                                 df['accX'])
            all_accX.append(normalized)
    except Exception as e:
        print(f"Skipping {file_path}: {str(e)}")

if not all_accX:
    print("No valid data found!")
    exit()

# Calculate mean and standard deviation
mean_accX = np.mean(all_accX, axis=0)
std_accX = np.std(all_accX, axis=0)

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(mean_accX, 'b-', linewidth=2, label='Mean Pattern')
plt.fill_between(range(len(mean_accX)),
                 mean_accX - std_accX,
                 mean_accX + std_accX,
                 color='blue', alpha=0.2, label='Variation Range')

plt.title("Common Pattern of All Spell Recordings (X-axis Acceleration)")
plt.xlabel("Normalized Time")
plt.ylabel("Acceleration")
plt.legend()
plt.grid(True)
plt.show()