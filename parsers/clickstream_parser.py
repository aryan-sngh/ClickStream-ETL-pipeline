import os
import json
from datetime import datetime
from logger_file.logger_config import etl_logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUARANTINE_DIR = os.path.join(BASE_DIR, "quarantine")
NULL_VALUES_DIR = os.path.join(BASE_DIR, "null_values")

os.makedirs(QUARANTINE_DIR, exist_ok=True)
os.makedirs(NULL_VALUES_DIR, exist_ok=True)

def quarantine_record(raw_data: str, reason: str):
    """Writes invalid or corrupted payloads to quarantine."""
    filename = f"quarantine_{datetime.utcnow().strftime('%Y%m%d')}.jsonl"
    file_path = os.path.join(QUARANTINE_DIR, filename)
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps({"reason": reason, "raw": raw_data, "quarantined_at": str(datetime.utcnow())}) + "\n")
    etl_logger.warning(f"Record quarantined: {reason}")

def log_null_record(data: dict, missing_field: str):
    """Stores records missing critical schema values."""
    filename = f"null_records_{datetime.utcnow().strftime('%Y%m%d')}.jsonl"
    file_path = os.path.join(NULL_VALUES_DIR, filename)
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps({"missing_field": missing_field, "record": data}) + "\n")
    etl_logger.warning(f"Null check failed for field: {missing_field}")

def parse_wikimedia_event(raw_line: str) -> dict | None:
    """Cleans, normalizes, and transforms Wikimedia event strings."""
    if not raw_line or not raw_line.strip():
        return None

    try:
        data = json.loads(raw_line)
    except json.JSONDecodeError as e:
        quarantine_record(raw_line, f"JSONDecodeError: {str(e)}")
        return None

    meta = data.get("meta", {})
    event_id = meta.get("id")
    raw_dt = meta.get("dt")

    if not event_id:
        log_null_record(data, "meta.id")
        return None

    # Parse and format ISO timestamp to MySQL DATETIME
    formatted_timestamp = None
    if raw_dt:
        try:
            clean_dt = raw_dt.replace("Z", "+00:00")
            dt_obj = datetime.fromisoformat(clean_dt)
            formatted_timestamp = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            formatted_timestamp = None

    if not formatted_timestamp:
        log_null_record(data, "meta.dt")
        return None

    length = data.get("length", {})
    length_old = length.get("old") if isinstance(length, dict) else None
    length_new = length.get("new") if isinstance(length, dict) else None
    length_change = (length_new - length_old) if (length_new is not None and length_old is not None) else None

    return {
        "event_id": str(event_id),
        "timestamp": formatted_timestamp,
        "event_type": data.get("type"),
        "wiki": data.get("wiki"),
        "user_name": data.get("user"),
        "is_bot": bool(data.get("bot", False)),
        "page_title": data.get("title"),
        "server_name": data.get("server_name"),
        "length_old": length_old,
        "length_new": length_new,
        "length_change": length_change
    }