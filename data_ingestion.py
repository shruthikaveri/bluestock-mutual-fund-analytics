import pandas as pd
from pathlib import Path

# Path to raw data folder
RAW_DATA_PATH = Path("data/raw")

# Get all CSV files
csv_files = list(RAW_DATA_PATH.glob("*.csv"))

print("\n===== BLUESTOCK DATA INGESTION =====\n")
print(f"Total CSV files found: {len(csv_files)}\n")

# Read and inspect every dataset
for file in csv_files:
    print("=" * 70)
    print(f"FILE: {file.name}")

    try:
        df = pd.read_csv(file)

        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")

        print("\nFirst 5 rows:")
        print(df.head())

        print("\nMissing values:")
        print(df.isnull().sum())

    except Exception as e:
        print(f"ERROR reading {file.name}: {e}")

    print("\n")

print("===== DATA INGESTION COMPLETED =====")