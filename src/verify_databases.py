
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_DIR = PROJECT_ROOT / "databases"

databases = {
    "institutions.db": "institutions",
    "hospitals.db": "hospitals",
    "restaurants.db": "restaurants",
}

for db_filename, table_name in databases.items():
    db_path = DB_DIR / db_filename

    print("\n" + "=" * 50)
    print(f"Database: {db_filename}")
    print("=" * 50)

    with sqlite3.connect(db_path) as conn:
        # Confirm that the table exists.
        tables = conn.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'table'"
        ).fetchall()

        print("Tables:", [table[0] for table in tables])

        # Count records.
        count = conn.execute(
            f'SELECT COUNT(*) FROM "{table_name}"'
        ).fetchone()[0]

        print("Total records:", f"{count:,}")

        # Display column names and types.
        columns = conn.execute(
            f'PRAGMA table_info("{table_name}")'
        ).fetchall()

        print("Schema:")
        for column in columns:
            print(f"  {column[1]}: {column[2]}")

        # Show one sample record.
        sample = conn.execute(
            f'SELECT * FROM "{table_name}" LIMIT 1'
        ).fetchone()

        print("Sample record:", sample)

print("\nDatabase verification completed!")
