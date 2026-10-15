
import sqlite3
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"
DB_DIR = PROJECT_ROOT / "databases"

DB_DIR.mkdir(parents=True, exist_ok=True)

# Explicit SQLite column types for each dataset.
SCHEMAS = {
    "institutions": {
        "institute_name": "TEXT",
        "eiin": "INTEGER",
        "institute_type": "TEXT",
        "division_id": "INTEGER",
        "division": "TEXT",
        "district_id": "INTEGER",
        "district": "TEXT",
        "thana_id": "INTEGER",
        "thana": "TEXT",
        "union_id": "INTEGER",
        "union_name": "TEXT",
        "mauza_id": "INTEGER",
        "mauza_name": "TEXT",
        "area_status": "TEXT",
        "geogrpycal_status": "TEXT",
        "address": "TEXT",
        "post": "TEXT",
        "management_type": "TEXT",
        "mobile": "TEXT",
        "student_type": "TEXT",
        "education_level": "TEXT",
        "affiliation": "TEXT",
        "mpo_status": "TEXT",
    },
    "hospitals": {
        "id": "INTEGER",
        "name": "TEXT",
        "name_bangla": "TEXT",
        "code": "REAL",
        "agency": "TEXT",
        "type": "TEXT",
        "division": "TEXT",
        "district": "TEXT",
        "city_corporation": "TEXT",
        "upazila": "TEXT",
        "paurasava": "TEXT",
        "union": "TEXT",
        "private": "INTEGER",
    },
    "restaurants": {
        "place_id": "TEXT",
        "name": "TEXT",
        "latitude": "REAL",
        "longitude": "REAL",
        "rating": "REAL",
        "number_of_reviews": "INTEGER",
        "affluence": "REAL",
        "address": "TEXT",
    },
}

for table_name, schema in SCHEMAS.items():
    csv_path = DATA_DIR / f"{table_name}.csv"
    db_path = DB_DIR / f"{table_name}.db"

    df = pd.read_csv(csv_path)

    # Match the schema to the CSV columns.
    assert list(df.columns) == list(schema.keys()), (
        f"Column mismatch in {table_name}: "
        f"{df.columns.tolist()}"
    )

    # Convert numeric fields while preserving missing values.
    for column, sql_type in schema.items():
        if sql_type == "INTEGER":
            df[column] = pd.to_numeric(
                df[column], errors="raise"
            ).astype("Int64")
        elif sql_type == "REAL":
            df[column] = pd.to_numeric(
                df[column], errors="raise"
            )

    column_definitions = ", ".join(
        f'"{column}" {sql_type}'
        for column, sql_type in schema.items()
    )

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            f'CREATE TABLE IF NOT EXISTS "{table_name}" '
            f'({column_definitions})'
        )

        # Rebuild the table so rerunning this script
        # replaces old records rather than duplicating them.
        conn.execute(f'DELETE FROM "{table_name}"')

        df.to_sql(
            table_name,
            conn,
            if_exists="append",
            index=False,
        )

        row_count = conn.execute(
            f'SELECT COUNT(*) FROM "{table_name}"'
        ).fetchone()[0]

    print(
        f"{table_name}: {row_count:,} rows saved "
        f"to {db_path.name}"
    )

print("\nAll three SQLite databases created successfully!")
