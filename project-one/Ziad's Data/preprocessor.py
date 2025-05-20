import pandas as pd
import glob
import os

# === Configurable Person Names ===
persons = ['Z', 'K']
gestures = ['Rock', 'Paper', 'Scissors']


# === Preprocessing Functions ===
def smooth_data(series, window_size=5):
    """ Apply a moving average filter to smooth the data. """
    return series.rolling(window=window_size).mean().bfill()


def interpolate_data(df, interval=0.05):
    """ Interpolates the dataframe to have consistent time intervals. """
    df['time_s'] = df['time'] / 1000
    df.set_index('time_s', inplace=True)

    # === 🔄 FIX: Remove any duplicates from the index
    df = df[~df.index.duplicated(keep='first')]

    # Generate a new consistent time index
    new_time_index = pd.RangeIndex(start=int(df.index.min() * 1000),
                                   stop=int(df.index.max() * 1000),
                                   step=int(interval * 1000)) / 1000

    # Reindex the DataFrame
    df = df.reindex(new_time_index)
    df.index.name = 'time_s'

    # === 🔄 FIX: Infer objects to avoid warnings
    df = df.infer_objects()

    # Interpolate missing values
    df.interpolate(method='linear', inplace=True)
    df.reset_index(inplace=True)

    return df


def preprocess_and_save():
    """ Load, preprocess, and save the cleaned CSVs for each person. """
    for person in persons:
        for gesture in gestures:
            csv_files = glob.glob(
                f"C:/Users/Ziad Morsy/PycharmProjects/group-c/project-one/Ziad's Data/{person}/{gesture}/*.csv")

            for file_path in csv_files:
                print(f"Preprocessing {file_path} for {person}...")
                df = pd.read_csv(file_path, sep=';')

                # Apply smoothing
                df['accX'] = smooth_data(df['accX'])
                df['accY'] = smooth_data(df['accY'])
                df['accZ'] = smooth_data(df['accZ'])
                df['gyroX'] = smooth_data(df['gyroX'])
                df['gyroY'] = smooth_data(df['gyroY'])
                df['gyroZ'] = smooth_data(df['gyroZ'])

                # Apply interpolation
                df = interpolate_data(df)

                # Save the new cleaned CSV
                filename = os.path.basename(file_path).replace(".csv", "_cleaned.csv")
                output_path = f"C:/Users/Ziad Morsy/PycharmProjects/group-c/project-one/Ziad's Data/{person}/{gesture}/{filename}"
                df.to_csv(output_path, sep=';', index=False)
                print(f"✅ Saved cleaned file: {output_path}")


preprocess_and_save()
