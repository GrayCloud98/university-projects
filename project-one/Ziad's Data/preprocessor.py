import pandas as pd
import glob
import os

# === Configurable Person Names ===
persons = ['Z', 'K']
gestures = ['Rock', 'Paper', 'Scissors']


# === Preprocessing Functions ===
def smooth_data(series, window_size=5):
    return series.rolling(window=window_size).mean().bfill()


def interpolate_data(df, interval=0.05):
    df['time_s'] = df['time'] / 1000
    df.set_index('time_s', inplace=True)
    df = df[~df.index.duplicated(keep='first')]

    new_time_index = pd.RangeIndex(start=int(df.index.min() * 1000),
                                   stop=int(df.index.max() * 1000),
                                   step=int(interval * 1000)) / 1000

    df = df.reindex(new_time_index)
    df.index.name = 'time_s'
    df = df.infer_objects()
    df.interpolate(method='linear', inplace=True)
    df.reset_index(inplace=True)
    return df


def preprocess_and_save():
    """ Load, preprocess, and save the cleaned CSVs to Cleaned/{gesture}/ folder """
    for person in persons:
        for gesture in gestures:
            csv_files = glob.glob(
                f"C:/Users/Ziad Morsy/PycharmProjects/group-c/project-one/Ziad's Data/{person}/{gesture}/*.csv")

            for file_path in csv_files:
                print(f"Preprocessing {file_path} for {person}...")
                df = pd.read_csv(file_path, sep=';')

                # Smoothing
                for axis in ['accX', 'accY', 'accZ', 'gyroX', 'gyroY', 'gyroZ']:
                    df[axis] = smooth_data(df[axis])

                # Interpolation
                df = interpolate_data(df)

                cleaned_folder = f"C:/Users/Ziad Morsy/PycharmProjects/group-c/project-one/Ziad's Data/Cleaned/{gesture}/"
                os.makedirs(cleaned_folder, exist_ok=True)

                filename = os.path.basename(file_path).replace(".csv", f"_{person}_cleaned.csv")
                output_path = os.path.join(cleaned_folder, filename)

                df.to_csv(output_path, sep=';', index=False)
                print(f"✅ Saved cleaned file: {output_path}")


preprocess_and_save()
