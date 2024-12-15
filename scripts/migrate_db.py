import sys
import os
from sqlalchemy import create_engine, text
from alembic import op
import sqlalchemy as sa

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from app.config import settings
from app.database.models import Base

def upgrade():
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.bind = engine
    
    # Drop existing tables
    Base.metadata.drop_all(engine)
    
    # Create new tables
    Base.metadata.create_all(engine)

    # Verify that all columns are created
    with engine.connect() as connection:
        result = connection.execute(text("PRAGMA table_info(messages)"))
        columns = [row[1] for row in result]
        print("Columns in messages table:", columns)

if __name__ == "__main__":
    upgrade()
    print("Database migration completed successfully.")

