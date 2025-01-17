from datetime import datetime
import sqlite3
from qcc_wfm_orthanc_cache.config import settings


def get_db_connection():
    """Context manager to manage SQLite connection."""
    return sqlite3.connect(settings.sqlite_file)
    

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create the table to track downloads and uploads
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS study_tracking (
        accession_number TEXT PRIMARY KEY,
        status TEXT,
        timestamp TEXT,
        error_message TEXT
    )
    ''')

    conn.commit()
    conn.close()

def log_status(accession_number: str, status: str, error_message: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert or update the status for the given accession number
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
    INSERT OR REPLACE INTO study_tracking (accession_number, status, timestamp, error_message)
    VALUES (?, ?, ?, ?)
    ''', (accession_number, status, timestamp, error_message))
    
    conn.commit()
    conn.close()
