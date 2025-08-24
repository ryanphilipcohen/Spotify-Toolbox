import sqlite3

"""
EXPLANATION:
This app uses a SQLite database to store user data, tracks, tags, and catalogs.
SQLite is easy to use, requiring minimal setup (with no server), sufficient for this app.
This file contains the functions used to work with the database.
"""


def get_connection():
    conn = sqlite3.connect("database.sqlite3")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            spotify_id TEXT UNIQUE,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        INSERT OR IGNORE INTO user (id, spotify_id) VALUES (?, ?)
            """,
        (1, "admin"),
    )

    cursor.execute(
        """
        DELETE FROM user WHERE spotify_id IS NULL
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS track (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            added_at TEXT,
            name TEXT NOT NULL,
            artists TEXT NOT NULL,
            album TEXT NOT NULL,
            album_id TEXT NOT NULL,
            duration_ms INTEGER NOT NULL,
            explicit BOOLEAN NOT NULL,
            popularity INTEGER NOT NULL,
            track_number INTEGER NOT NULL,
            release_date TEXT NOT NULL,
            image TEXT NOT NULL,
            spotify_id TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user(id)
            UNIQUE(user_id, added_at)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tag (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            parent INTEGER DEFAULT NULL,
            locked BOOLEAN DEFAULT FALSE,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user(id)
        )
        """
    )

    cursor.execute(
        """
        INSERT OR IGNORE INTO tag (id, user_id, name, type, locked) VALUES (?, ?, ?, ?, ?)
            """,
        (1, 1, "root", "admin", True),
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS catalog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user(id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS track_tag (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            track_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            is_tagged BOOLEAN DEFAULT FALSE,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (track_id) REFERENCES track(id),
            FOREIGN KEY (tag_id) REFERENCES tag(id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS catalog_track_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            catalog_id INTEGER NOT NULL,
            track_id INTEGER NOT NULL,
            catalog_index INTEGER NOT NULL,
            completed BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (catalog_id) REFERENCES catalog(id),
            FOREIGN KEY (track_id) REFERENCES track(id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS catalog_track_filter (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            catalog_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            rule TEXT NOT NULL,
            FOREIGN KEY (catalog_id) REFERENCES catalog(id),
            FOREIGN KEY (tag_id) REFERENCES tag(id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS catalog_tag_filter (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            catalog_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            FOREIGN KEY (catalog_id) REFERENCES catalog(id),
            FOREIGN KEY (tag_id) REFERENCES tag(id)
        )
        """
    )

    conn.commit()
    conn.close()
