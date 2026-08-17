CREATE DATABASE IF NOT EXISTS clickstream_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE clickstream_db;

CREATE TABLE IF NOT EXISTS clickstream_events (
    event_id VARCHAR(100) PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    event_type VARCHAR(50),
    wiki VARCHAR(50),
    user_name VARCHAR(255),
    is_bot BOOLEAN DEFAULT FALSE,
    page_title TEXT,
    server_name VARCHAR(100),
    length_old INT NULL,
    length_new INT NULL,
    length_change INT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_events_timestamp (timestamp),
    INDEX idx_events_wiki (wiki),
    INDEX idx_events_user (user_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;