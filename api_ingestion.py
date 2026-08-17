import os
import requests
from sseclient import SSEClient
from dotenv import load_dotenv
from logger_file.logger_config import ingestion_logger
from parsers.clickstream_parser import parse_wikimedia_event
from db.db_writes import insert_event

load_dotenv()

STREAM_URL = os.getenv("STREAM_URL", "https://stream.wikimedia.org/v2/stream/recentchange")
USER_AGENT = os.getenv("USER_AGENT", "ClickstreamETLPipeline/1.0 (contact@example.com)")

def run_stream_ingestion(max_events: int = 50):
    """Consumes SSE stream, transforms payload, and writes to MySQL."""
    headers = {"User-Agent": USER_AGENT}
    ingestion_logger.info(f"Connecting to SSE stream: {STREAM_URL}")

    try:
        response = requests.get(STREAM_URL, headers=headers, stream=True, timeout=30)
        client = SSEClient(response)
        count = 0

        for event in client.events():
            if event.event == "message":
                try:
                    parsed = parse_wikimedia_event(event.data)
                    if parsed:
                        insert_event(parsed)
                        count += 1

                    if max_events and count >= max_events:
                        ingestion_logger.info(f"Batch completed with {count} records.")
                        break
                except Exception as e:
                    ingestion_logger.error(f"Error handling event line: {e}")

    except Exception as e:
        ingestion_logger.critical(f"Streaming error: {e}")
        raise

if __name__ == "__main__":
    run_stream_ingestion(max_events=20)