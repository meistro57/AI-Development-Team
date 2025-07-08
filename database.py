import os
import sqlite3
from contextlib import closing

DB_PATH = os.getenv("DB_PATH", os.path.join(os.getcwd(), "projects.db"))


def init_db():
    """Initialize the SQLite database"""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                description TEXT,
                path TEXT,
                created TEXT
            )"""
        )
        conn.commit()


def add_project(name: str, description: str, path: str, created: str) -> None:
    """Add a project to the database"""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute(
            "INSERT INTO projects (name, description, path, created) VALUES (?, ?, ?, ?)",
            (name, description, path, created),
        )
        conn.commit()


def list_projects() -> list[tuple[str, str]]:
    """Return list of project name/description tuples"""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.execute("SELECT name, description FROM projects ORDER BY id DESC")
        return cur.fetchall()


def list_projects_full() -> list[tuple[str, str, str, str]]:
    """Return list of all project details"""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.execute(
            "SELECT name, description, path, created FROM projects ORDER BY id DESC"
        )
        return cur.fetchall()


def get_project(name: str) -> tuple | None:
    """Retrieve single project info"""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.execute(
            "SELECT name, description, path, created FROM projects WHERE name=?",
            (name,),
        )
        return cur.fetchone()


def delete_project(name: str) -> None:
    """Remove a project from the database"""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute("DELETE FROM projects WHERE name=?", (name,))
        conn.commit()
