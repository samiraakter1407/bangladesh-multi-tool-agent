
import pandas as pd
from pathlib import Path

# Project root is the parent of the src folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"

files = {
    "Institutions": "institutions.csv",
    "Hospitals": "hospitals.csv",
    "Restaurants": "restaurants.csv",
}

for dataset_name, filename in files.items():
    file_path = DATA_DIR / filename

    print("\n" + "=" * 60)
    print(f"DATASET: {dataset_name}")
    print("=" * 60)

    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}")
        continue

    df = pd.read_csv(file_path)

    print("Number of rows:", len(df))
    print("Number of columns:", len(df.columns))

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values per column:")
    print(df.isnull().sum())

    print("\nFirst 3 records:")
    print(df.head(3).to_string(index=False))
