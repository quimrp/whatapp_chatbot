import sqlite3
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from app.config import settings

def update_schema():
    conn = sqlite3.connect(settings.DATABASE_URL.replace("sqlite:///", ""))
    cursor = conn.cursor()

    try:
        # Update media_messages table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS media_messages_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id TEXT,
            media_id TEXT,
            link TEXT
        )
        """)

        # Get existing columns from media_messages table
        cursor.execute("PRAGMA table_info(media_messages)")
        existing_columns = [row[1] for row in cursor.fetchall()]

        # Prepare columns for insertion
        columns_to_insert = [col for col in ['id', 'message_id', 'media_id', 'link'] if col in existing_columns]
        columns_string = ', '.join(columns_to_insert)

        # Copy data from the old table to the new table (if it exists)
        if existing_columns:
            cursor.execute(f"""
            INSERT OR IGNORE INTO media_messages_new ({columns_string})
            SELECT {columns_string} FROM media_messages
            """)


        # Drop the old table and rename the new one
        cursor.execute("DROP TABLE IF EXISTS media_messages")
        cursor.execute("ALTER TABLE media_messages_new RENAME TO media_messages")

        # Ensure other tables are up to date
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            waba_id TEXT,
            phone_number_id TEXT,
            from_number TEXT,
            "to" TEXT,
            pushname TEXT,
            type TEXT,
            body TEXT,
            time TEXT,
            raw_data TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS quoted_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id TEXT,
            quoted_data TEXT
        )
        """)

        conn.commit()
        print("Database schema updated successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    update_schema()

