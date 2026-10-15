
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

datasets = {
    "institutions": "institutions.csv",
    "hospitals": "hospitals.csv",
    "restaurants": "restaurants.csv",
}

for dataset_name, filename in datasets.items():
    input_path = RAW_DIR / filename

    df = pd.read_csv(input_path)

    # Standardize column names for easier SQL queries.
    df.columns = [
        col.strip()
        .lower()
        .replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
        for col in df.columns
    ]

    # Preserve all rows; represent missing values as nulls.
    df = df.convert_dtypes()

    output_path = PROCESSED_DIR / f"{dataset_name}.csv"
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"\nDataset: {dataset_name}")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))
    print("Saved:", output_path)
    print("Column names:", df.columns.tolist())

print("\nAll datasets prepared successfully!")
