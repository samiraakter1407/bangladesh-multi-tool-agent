
import sqlite3
from pathlib import Path
from langchain_core.tools import tool

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "databases" / "restaurants.db"


def search_restaurants(
    location: str = "",
    name: str = "",
    min_rating: float = 0,
    limit: int = 10,
) -> str:
    """Search restaurant and place records."""

    limit = max(1, min(int(limit), 50))
    min_rating = max(0.0, min(float(min_rating), 5.0))

    conditions = []
    params = []

    if location.strip():
        conditions.append(
            "LOWER(COALESCE(address, '')) LIKE ?"
        )
        params.append(f"%{location.strip().lower()}%")

    if name.strip():
        conditions.append(
            "LOWER(COALESCE(name, '')) LIKE ?"
        )
        params.append(f"%{name.strip().lower()}%")

    if min_rating > 0:
        conditions.append("rating >= ?")
        params.append(min_rating)

    where_clause = (
        "WHERE " + " AND ".join(conditions)
        if conditions else ""
    )

    query = f"""
        SELECT name, address, rating, number_of_reviews,
               latitude, longitude
        FROM restaurants
        {where_clause}
        ORDER BY rating DESC
        LIMIT ?
    """
    params.append(limit)

    count_query = f"""
        SELECT COUNT(*)
        FROM restaurants
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
        return "No matching places found in the dataset."

    output = [
        f"Found {total:,} matching places. "
        f"Showing {len(rows)}:"
    ]

    for row in rows:
        rating = (
            f"{row['rating']:.1f}/5"
            if row["rating"] is not None
            else "Not available"
        )

        reviews = (
            str(int(row["number_of_reviews"]))
            if row["number_of_reviews"] is not None
            else "Not available"
        )

        output.append(
            f"\nName: {row['name']}"
            f"\nAddress: {row['address']}"
            f"\nRating: {rating}"
            f"\nReviews: {reviews}"
            f"\nCoordinates: {row['latitude']}, "
            f"{row['longitude']}"
        )

    return "\n".join(output)


@tool
def restaurants_db_tool(
    location: str = "",
    name: str = "",
    min_rating: float = 0,
    limit: int = 10,
) -> str:
    """Search the Bangladesh restaurant and places database.

    Search by name, address text, or minimum rating.
    Use for questions about recorded place details and ratings.
    Cuisine filtering is not supported by this dataset.
    """
    return search_restaurants(
        location=location,
        name=name,
        min_rating=min_rating,
        limit=limit,
    )


if __name__ == "__main__":
    print(
        search_restaurants(
            location="Dhaka",
            min_rating=4,
            limit=5,
        )
    )
