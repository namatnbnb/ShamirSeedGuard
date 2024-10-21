from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from cryptography.fernet import Fernet
import os
from datetime import datetime, timedelta

Base = declarative_base()
engine = create_engine('sqlite:///shares.db')
Session = sessionmaker(bind=engine)

class EncryptedShare(Base):
    __tablename__ = 'encrypted_shares'

    id = Column(Integer, primary_key=True)
    share_id = Column(String(50), unique=True, nullable=False)
    encrypted_share = Column(Text, nullable=False)
    time_lock = Column(DateTime, nullable=True)

# Generate a key for encryption (in a real-world scenario, this should be stored securely)
ENCRYPTION_KEY = Fernet.generate_key()

def encrypt_share(share):
    f = Fernet(ENCRYPTION_KEY)
    return f.encrypt(share.encode()).decode()

def decrypt_share(encrypted_share):
    f = Fernet(ENCRYPTION_KEY)
    return f.decrypt(encrypted_share.encode()).decode()

# Create the database and tables
Base.metadata.create_all(engine)
