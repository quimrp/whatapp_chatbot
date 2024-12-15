import sys
import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
import logging

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from app.config import settings
from app.database.models import Base, Message, InteractiveMessage, MultimediaMessage, Order, OrderItem

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def clear_database():
    logger.info("Starting database clearing process")

    # Create engine and session
    engine = create_engine(settings.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Get all table names
        inspector = inspect(engine)
        table_names = inspector.get_table_names()

        # Delete all records from each table
        for table_name in table_names:
            logger.info(f"Clearing table: {table_name}")
            session.execute(f"DELETE FROM {table_name}")

        # Commit the changes
        session.commit()
        logger.info("All data has been cleared from the database")

    except Exception as e:
        logger.error(f"An error occurred while clearing the database: {str(e)}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    clear_database()

