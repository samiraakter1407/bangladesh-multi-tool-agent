
import sqlite3
from pathlib import Path
from langchain_core.tools import tool

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "databases" / "hospitals.db"


def search_hospitals(
    location: str = "",
    facility_type: str = "",
    name: str = "",
    limit: int = 10,
) -> str:
    """Search hospital and health-facility records."""

    limit = max(1, min(int(limit), 50))

    conditions = []
    params = []

    if location.strip():
        conditions.append(
            """
            (
                LOWER(COALESCE(division, '')) LIKE ?
                OR LOWER(COALESCE(district, '')) LIKE ?
                OR LOWER(COALESCE(upazila, '')) LIKE ?
                OR LOWER(COALESCE(city_corporation, '')) LIKE ?
            )
            """
        )
        term = f"%{location.strip().lower()}%"
        params.extend([term, term, term, term])

    if facility_type.strip():
        conditions.append(
            "LOWER(COALESCE(type, '')) LIKE ?"
        )
        params.append(f"%{facility_type.strip().lower()}%")

    if name.strip():
        conditions.append(
            "LOWER(COALESCE(name, '')) LIKE ?"
        )
        params.append(f"%{name.strip().lower()}%")

    where_clause = (
        "WHERE " + " AND ".join(conditions)
        if conditions
        else ""
    )

    query = f"""
        SELECT name, type, agency, division, district,
               upazila, private
        FROM hospitals
        {where_clause}
        ORDER BY name
        LIMIT ?
    """
    params.append(limit)

    try:
        with sqlite3.connect(
            f"file:{DB_PATH.as_posix()}?mode=ro",
            uri=True,
        ) as conn:
            conn.row_factory = sqlite3.Row

            rows = conn.execute(query, params).fetchall()

            count_query = f"""
                SELECT COUNT(*)
                FROM hospitals
                {where_clause}
            """
            total = conn.execute(
                count_query, params[:-1]
            ).fetchone()[0]

    except sqlite3.Error as error:
        return f"Database query failed: {error}"

    if not rows:
        return "No matching facilities found in the dataset."

    output = [
        f"Found {total:,} matching records. "
        f"Showing {len(rows)}:"
    ]

    for row in rows:
        output.append(
            f"\nName: {row['name']}"
            f"\nType: {row['type']}"
            f"\nAgency: {row['agency'] or 'Not available'}"
            f"\nDivision: {row['division']}"
            f"\nDistrict: {row['district']}"
            f"\nUpazila: {row['upazila'] or 'Not available'}"
            f"\nPrivate flag: {row['private']}"
        )

    return "\n".join(output)

@tool
def hospitals_db_tool(
    location: str = "",
    facility_type: str = "",
    name: str = "",
    limit: int = 10,
) -> str:
    """Search the Bangladesh hospital database.

    Use for questions about health facilities, their names,
    facility types, administrative locations, and agencies.
    Supports location, facility type, and name filters.
    """
    return search_hospitals(
        location=location,
        facility_type=facility_type,
        name=name,
        limit=limit,
    )


if __name__ == "__main__":
    print(search_hospitals(location="Dhaka", limit=5))
