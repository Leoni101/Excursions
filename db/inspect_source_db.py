import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DB = BASE_DIR / "data" / "excursion.sqlite"


def inspect_database():
    if not SOURCE_DB.exists():
        print(f"Файл базы данных не найден: {SOURCE_DB}")
        return

    conn = sqlite3.connect(SOURCE_DB)
    cursor = conn.cursor()

    tables = cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    ).fetchall()

    print(f"Инспекция исходной БД: {SOURCE_DB.name}")
    for (table_name,) in tables:
        count = cursor.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        columns = [
            col[1] for col in cursor.execute(f"PRAGMA table_info({table_name})").fetchall()
        ]
        print(f" - Таблица '{table_name}': записей = {count}, поля = {columns}")

    conn.close()


if __name__ == "__main__":
    inspect_database()