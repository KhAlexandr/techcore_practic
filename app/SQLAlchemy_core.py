from sqlalchemy import text
from database import session_maker


async def get_books_report():
    async with session_maker() as session:
        sql = text(
            """
            SELECT 
                a.first_name || ' ' || a.last_name as author_name,
                COUNT(b.id) as book_count,
                AVG(b.year) as avg_year,
                MIN(b.year) as first_book,
                MAX(b.year) as latest_book
            FROM authors a
            LEFT JOIN books b ON a.id = b.author_id
            GROUP BY a.id, author_name
            HAVING COUNT(b.id) > 0
            ORDER BY book_count DESC
        """
        )

        result = await session.execute(sql)
        return result.mappings().all()
