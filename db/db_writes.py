from sqlalchemy import text
from db.db_connection import engine
from logger_file.logger_config import db_logger

def insert_event(event_data: dict) -> bool:
    """Inserts a normalized clickstream event into MySQL."""
    query = text("""
        INSERT IGNORE INTO clickstream_events (
            event_id, timestamp, event_type, wiki, user_name,
            is_bot, page_title, server_name, length_old, length_new, length_change
        ) VALUES (
            :event_id, :timestamp, :event_type, :wiki, :user_name,
            :is_bot, :page_title, :server_name, :length_old, :length_new, :length_change
        );
    """)

    try:
        with engine.begin() as conn:
            conn.execute(query, event_data)
            db_logger.info(f"Committed event ID: {event_data.get('event_id')}")
        return True
    except Exception as e:
        db_logger.error(f"MySQL write failed for event {event_data.get('event_id')}: {e}")
        return False