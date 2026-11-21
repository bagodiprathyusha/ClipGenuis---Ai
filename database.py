
import sqlite3

def create_database():
    conn = sqlite3.connect("brand_memory.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS brand_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand_name TEXT,
            tone TEXT,
            hashtags TEXT,
            caption_style TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_brand(brand_name, tone, hashtags, caption_style):
    conn = sqlite3.connect("brand_memory.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO brand_memory
        (brand_name, tone, hashtags, caption_style)
        VALUES (?, ?, ?, ?)
    """, (brand_name, tone, hashtags, caption_style))

    conn.commit()
    conn.close()


def get_brand():
    conn = sqlite3.connect("brand_memory.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM brand_memory ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()

    conn.close()
    return result


create_database()
