import sqlite3
import sys
import os
import logging

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from app.config import settings

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def verify_schema():
    try:
        conn = sqlite3.connect(settings.DATABASE_URL.replace("sqlite:///", ""))
        cursor = conn.cursor()

        # Get table info for multimedia_messages
        cursor.execute("PRAGMA table_info(multimedia_messages)")
        columns = cursor.fetchall()

        logger.info("Current 'multimedia_messages' table schema:")
        for column in columns:
            logger.info(f"Column: {column[1]}, Type: {column[2]}, Nullable: {column[3]}, Default: {column[4]}, Primary Key: {column[5]}")

        # Check if media_url is present
        if 'media_url' not in [column[1] for column in columns]:
            logger.warning("'media_url' column is missing from the multimedia_messages table!")
        else:
            logger.info("'media_url' column is present in the multimedia_messages table.")

        # Check other important columns
        expected_columns = ['id', 'message_id', 'media_type', 'media_id', 'media_url']
        missing_columns = [col for col in expected_columns if col not in [column[1] for column in columns]]
        
        if missing_columns:
            logger.warning(f"The following columns are missing: {', '.join(missing_columns)}")
        else:
            logger.info("All expected columns are present in the multimedia_messages table.")

    except sqlite3.Error as e:
        logger.error(f"An error occurred while connecting to the database: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    verify_schema()

