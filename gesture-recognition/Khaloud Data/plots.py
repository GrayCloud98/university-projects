import pandas as pd
import matplotlib.pyplot as plt

# Load CSV and use semicolon separator
df = pd.read_csv("Avada Kedavra/recording-20250506-171134.csv", sep=';')


# Convert time from ms to seconds
df['time_s'] = df['time'] / 1000

# Plot
plt.figure(figsize=(12, 6))

# Plot Accelerometer
plt.subplot(2, 1, 1)
plt.plot(df['time_s'], df['accX'], label='accX')
plt.plot(df['time_s'], df['accY'], label='accY')
plt.plot(df['time_s'], df['accZ'], label='accZ')
plt.title('Accelerometer Data')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration')
plt.legend()

# Plot Gyroscope
plt.subplot(2, 1, 2)
plt.plot(df['time_s'], df['gyroX'], label='gyroX')
plt.plot(df['time_s'], df['gyroY'], label='gyroY')
plt.plot(df['time_s'], df['gyroZ'], label='gyroZ')
plt.title('Gyroscope Data')
plt.xlabel('Time (s)')
plt.ylabel('Rotation Rate')
plt.legend()

plt.tight_layout()
plt.show()