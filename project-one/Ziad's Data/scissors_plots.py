import pandas as pd
import matplotlib.pyplot as plt
import glob


def plot_sensor_data(file_path):
    # Load CSV and use semicolon separator
    df = pd.read_csv(file_path, sep=';')

    # Convert time from ms to seconds
    df['time_s'] = df['time'] / 1000

    # Plot
    plt.figure(figsize=(12, 6))

    # Plot Accelerometer
    plt.subplot(2, 1, 1)
    plt.plot(df['time_s'], df['accX'], label='accX')
    plt.plot(df['time_s'], df['accY'], label='accY')
    plt.plot(df['time_s'], df['accZ'], label='accZ')
    plt.title(f'Accelerometer Data - {file_path}')
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration')
    plt.legend()

    # Plot Gyroscope
    plt.subplot(2, 1, 2)
    plt.plot(df['time_s'], df['gyroX'], label='gyroX')
    plt.plot(df['time_s'], df['gyroY'], label='gyroY')
    plt.plot(df['time_s'], df['gyroZ'], label='gyroZ')
    plt.title(f'Gyroscope Data - {file_path}')
    plt.xlabel('Time (s)')
    plt.ylabel('Rotation Rate')
    plt.legend()

    plt.tight_layout()
    plt.show()


# Automatically find all CSV files in the folder
csv_files = glob.glob("Scissors/*.csv")

# Set the maximum number of files to plot
MAX_PLOTS = 5

# Loop through all CSV files and plot them (limited to MAX_PLOTS)
for file in csv_files[:MAX_PLOTS]:
    plot_sensor_data(file)
