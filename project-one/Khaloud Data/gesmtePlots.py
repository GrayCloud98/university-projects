import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# Set the directory where your CSV files are stored
directory = "C:/Users/Admin/PycharmProjects/group-c/project-one/Khaloud Data/Rock"

# Get all CSV files in the directory
csv_files = glob.glob(os.path.join(directory, "recording-*.csv"))

# Check if any files were found
if not csv_files:
    print("No CSV files found in the directory!")
    exit()

# Create a figure for all plots
plt.figure(figsize=(14, 8))

# Process each file
for file_path in csv_files:
    try:
        # Read CSV with semicolon delimiter
        df = pd.read_csv(file_path, delimiter=';')

        # Extract file name for labeling
        file_name = os.path.basename(file_path)

        # Plot accelerometer data if columns exist
        if all(col in df.columns for col in ['accX', 'accY', 'accZ']):
            plt.plot(df['accX'], label=f"{file_name} - accX")
            plt.plot(df['accY'], label=f"{file_name} - accY")
            plt.plot(df['accZ'], label=f"{file_name} - accZ")

    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        continue

# Add plot elements
plt.title("Magic Hand - All Spell Recordings (Accelerometer Data)")
plt.xlabel("Time Index")
plt.ylabel("Acceleration Value")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()
