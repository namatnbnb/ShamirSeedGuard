import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, Column, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table
from sqlalchemy.sql import text
from models import EncryptedShare

engine = create_engine('sqlite:///shares.db')
Base = declarative_base()

def upgrade():
    # Create a new metadata object
    metadata = MetaData()
    
    # Reflect the existing table
    encrypted_shares = Table('encrypted_shares', metadata, autoload_with=engine)
    
    # Check if the column already exists
    if 'time_lock' not in encrypted_shares.columns:
        # Add the new column
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE encrypted_shares ADD COLUMN time_lock DATETIME"))
        print("Added 'time_lock' column to 'encrypted_shares' table")
    else:
        print("'time_lock' column already exists in 'encrypted_shares' table")

if __name__ == '__main__':
    upgrade()
