"""Setup script for Neon Postgres database."""
import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import psycopg2
from app.config import settings


def create_feedback_table():
    """Create feedback table with indexes in Neon Postgres."""
    try:
        conn = psycopg2.connect(settings.neon_database_url)
        cursor = conn.cursor()

        # Create feedback table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                query TEXT NOT NULL,
                response TEXT NOT NULL,
                selected_text TEXT,
                rating INTEGER NOT NULL CHECK (rating IN (1, -1)),
                comment TEXT,
                timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
                session_id VARCHAR(255),
                sources_json JSONB,
                CONSTRAINT query_length CHECK (LENGTH(query) <= 2000),
                CONSTRAINT comment_length CHECK (comment IS NULL OR LENGTH(comment) <= 1000)
            );
        """)

        # Create indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_feedback_timestamp ON feedback(timestamp);
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_feedback_rating ON feedback(rating);
        """)

        conn.commit()
        cursor.close()
        conn.close()

        print("✅ Feedback table created successfully")
        print("✅ Indexes created: idx_feedback_timestamp, idx_feedback_rating")
        return True

    except Exception as e:
        print(f"❌ Error creating feedback table: {e}")
        return False


if __name__ == "__main__":
    create_feedback_table()
