import os
import sqlite3
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).parents[1]


def run_alembic(database_path: Path, *arguments: str) -> None:
    environment = os.environ.copy()
    environment["DATABASE_URL"] = f"sqlite:///{database_path}"
    subprocess.run(
        [sys.executable, "-m", "alembic", *arguments],
        cwd=PROJECT_ROOT,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )


def test_alembic_upgrade_creates_conversations_schema(tmp_path: Path) -> None:
    database_path = tmp_path / "migrations.db"

    run_alembic(database_path, "upgrade", "head")

    connection = sqlite3.connect(database_path)
    tables = {
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )
    }
    columns = {
        row[1]
        for row in connection.execute("PRAGMA table_info(conversations)")
    }
    indexes = {
        row[1]
        for row in connection.execute("PRAGMA index_list(conversations)")
    }
    connection.close()

    assert "conversations" in tables
    assert {
        "id",
        "phone_number",
        "incoming_message",
        "llm_response",
        "provider_message_id",
        "status",
        "created_at",
        "feedback",
    } <= columns
    assert "ix_conversations_phone_number" in indexes


def test_alembic_downgrade_removes_conversations_schema(tmp_path: Path) -> None:
    database_path = tmp_path / "migrations.db"

    run_alembic(database_path, "upgrade", "head")
    run_alembic(database_path, "downgrade", "base")

    connection = sqlite3.connect(database_path)
    tables = {
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )
    }
    connection.close()

    assert "conversations" not in tables
