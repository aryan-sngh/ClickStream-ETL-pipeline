# ⚡ Real-Time Wikimedia Clickstream Pipeline (ETL)

A data engineering pipeline built to consume, transform, and store real-time event streams from Wikipedia (Wikimedia) changes, automated with Apache Airflow and persisted into MySQL.

---

## 💡 Motivation & Problem Statement

Wikipedia generates thousands of edits, page creations, and bot actions every minute worldwide. Analyzing these changes in real time requires handling continuous event streams rather than static batch files. 

This project demonstrates how to:
1. Tap into a live server-sent event (SSE) stream without overwhelming the consumer.
2. Clean and structure nested JSON event payloads into relational rows.
3. Schedule micro-batch ingestion runs using Apache Airflow to keep data fresh in a MySQL store for analytics.

---

## 🏗️ Architecture & Data Flow

```text
 ┌───────────────────────────┐
 │ Wikimedia EventStream API │ (SSE HTTP Stream)
 └─────────────┬─────────────┘
               │
               ▼
 ┌───────────────────────────┐
 │      api_ingestion.py     │ • Opens persistent stream connection
 │  (Extract & Transform)    │ • Extracts user flags, page titles, byte changes
 └─────────────┬─────────────┘ • Batches events to prevent socket exhaustion
               │
               ▼
 ┌───────────────────────────┐
 │      db/db_writes.py      │ • SQLAlchemy engine connection pool
 │        (Load Layer)       │ • Inserts structured records into MySQL
 └─────────────┬─────────────┘
               │
               ▼
 ┌───────────────────────────┐
 │       MySQL Database      │ (clickstream_events table)
 └─────────────▲─────────────┘
               │
 ┌─────────────┴─────────────┐
 │    Apache Airflow DAG     │ • Controls execution schedule
 │   (Orchestration Layer)   │ • Handles retries, task logging & observability
 └───────────────────────────┘
