
import sqlite3
from pathlib import Path
from langchain_core.tools import tool

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "databases" / "institutions.db"


def search_institutions(
    location: str = "",
    institution_type: str = "",
    education_level: str = "",
    name: str = "",
    limit: int = 10,
) -> str:
    """Search educational institutions in Bangladesh."""

    limit = max(1, min(int(limit), 50))
    conditions = []
    params = []

    if location.strip():
        term = f"%{location.strip().lower()}%"
        conditions.append("""
            (
                LOWER(COALESCE(division, '')) LIKE ?
                OR LOWER(COALESCE(district, '')) LIKE ?
                OR LOWER(COALESCE(thana, '')) LIKE ?
            )
        """)
        params.extend([term, term, term])

    if institution_type.strip():
        conditions.append(
            "LOWER(COALESCE(institute_type, '')) LIKE ?"
        )
        params.append(f"%{institution_type.strip().lower()}%")

    if education_level.strip():
        conditions.append(
            "LOWER(COALESCE(education_level, '')) LIKE ?"
        )
        params.append(f"%{education_level.strip().lower()}%")

    if name.strip():
        conditions.append(
            "LOWER(COALESCE(institute_name, '')) LIKE ?"
        )
        params.append(f"%{name.strip().lower()}%")

    where_clause = (
        "WHERE " + " AND ".join(conditions)
        if conditions else ""
    )

    query = f"""
        SELECT institute_name, eiin, institute_type,
               division, district, thana,
               management_type, education_level, address
        FROM institutions
        {where_clause}
        ORDER BY institute_name
        LIMIT ?
    """
    params.append(limit)

    count_query = f"""
        SELECT COUNT(*)
        FROM institutions
        {where_clause}
    """

    try:
        with sqlite3.connect(
            f"file:{DB_PATH.as_posix()}?mode=ro",
            uri=True,
        ) as conn:
            conn.row_factory = sqlite3.Row

            total = conn.execute(
                count_query, params[:-1]
            ).fetchone()[0]

            rows = conn.execute(query, params).fetchall()

    except sqlite3.Error as error:
        return f"Database query failed: {error}"

    if not rows:
        return "No matching institutions found in the dataset."

    output = [
        f"Found {total:,} matching institutions. "
        f"Showing {len(rows)}:"
    ]

    for row in rows:
        output.append(
            f"\nName: {row['institute_name']}"
            f"\nEIIN: {row['eiin']}"
            f"\nType: {row['institute_type']}"
            f"\nDivision: {row['division']}"
            f"\nDistrict: {row['district']}"
            f"\nThana: {row['thana']}"
            f"\nManagement: {row['management_type']}"
            f"\nEducation level: {row['education_level']}"
            f"\nAddress: {row['address'] or 'Not available'}"
        )

    return "\n".join(output)


@tool
def institutions_db_tool(
    location: str = "",
    institution_type: str = "",
    education_level: str = "",
    name: str = "",
    limit: int = 10,
) -> str:
    """Search Bangladesh's institutional database.

    Use for institution names, EIINs, institution types,
    locations, management types, and education levels.
    """
    return search_institutions(
        location=location,
        institution_type=institution_type,
        education_level=education_level,
        name=name,
        limit=limit,
    )


if __name__ == "__main__":
    print(search_institutions(
        location="Dhaka",
        institution_type="College",
        limit=5,
    ))
