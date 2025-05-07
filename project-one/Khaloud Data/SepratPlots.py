import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

directory = "C:/Users/Admin/PycharmProjects/group-c/project-one/Khaloud Data/Rock"
csv_files = glob.glob(os.path.join(directory, "recording-*.csv"))

if not csv_files:
    print("No CSV files found in the directory!")
    exit()

for file_path in csv_files:
    try:
        df = pd.read_csv(file_path, delimiter=';')
        file_name = os.path.basename(file_path)

        plt.figure(figsize=(10, 6))

        if all(col in df.columns for col in ['accX', 'accY', 'accZ']):
            plt.plot(df['accX'], label='X-axis')
            plt.plot(df['accY'], label='Y-axis')
            plt.plot(df['accZ'], label='Z-axis')

            plt.title(f"Accelerometer Data: {file_name}")
            plt.xlabel("Time Index")
            plt.ylabel("Acceleration")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.show()

    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        continue