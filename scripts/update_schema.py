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
        # Create messages table (if not exists)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wamid TEXT UNIQUE,
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

        # Create interactive_messages table (if not exists)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS interactive_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id INTEGER,
            interactive_type TEXT,
            content TEXT,
            FOREIGN KEY (message_id) REFERENCES messages(id)
        )
        """)

        # Create multimedia_messages table (if not exists)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS multimedia_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id INTEGER,
            media_type TEXT,
            media_id TEXT,
            media_url TEXT,
            FOREIGN KEY (message_id) REFERENCES messages(id)
        )
        """)

        # Create orders table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id INTEGER,
            catalog_id TEXT,
            status TEXT CHECK(status IN ('recibido', 'preparacion', 'enviado', 'entregado')),
            FOREIGN KEY (message_id) REFERENCES messages(id)
        )
        """)

        # Create order_items table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_retailer_id TEXT,
            quantity INTEGER,
            item_price REAL,
            currency TEXT,
            FOREIGN KEY (order_id) REFERENCES orders(id)
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

