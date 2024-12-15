import sqlite3
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from app.config import settings

def verify_schema():
    conn = sqlite3.connect(settings.DATABASE_URL.replace("sqlite:///", ""))
    cursor = conn.cursor()

    # Get table info
    cursor.execute("PRAGMA table_info(messages)")
    columns = cursor.fetchall()

    print("Current 'messages' table schema:")
    for column in columns:
        print(f"Column: {column[1]}, Type: {column[2]}")

    conn.close()

if __name__ == "__main__":
    verify_schema()

