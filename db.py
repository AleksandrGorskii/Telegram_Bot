import sqlite3
from typing import Any


def create_tables() -> None:
    with sqlite3.connect('peoples.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS people("
            "date TEXT, "
            "time TEXT, "
            "title TEXT, "
            "name VARCHAR(50), "
            "surname VARCHAR(60), "
            "history VARCHAR(500))"
        )


        cursor.execute(
            "CREATE TABLE IF NOT EXISTS people_info("
            "date TEXT, "
            "time TEXT, "
            "title TEXT, "
            "name VARCHAR(50), "
            "surname VARCHAR(60), "
            "history VARCHAR(500))"
        )


def add_info(name: str, surname: str) -> list[str]:
    lst = []
    with sqlite3.connect('peoples.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute("SELECT date, time, title FROM people WHERE name = ? AND surname = ?", (name, surname))
        for i in cursor.fetchall():
            res = str(i).replace('(', '').replace(')', '') + '\n'
            lst.append(res)
    return lst


def search_info(date_now_str: str, time_now_str: str, query: Any, name: str, surname: str, history: Any) -> None:
    with sqlite3.connect('peoples.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute("INSERT INTO people(date, time, title, name, surname, history) VALUES(?, ?, ?, ?, ?, ?)",
                       (date_now_str, time_now_str, query, name, surname, history))


def record_info(date_now_str: str, time_now_str: str, history: Any, name: str, surname: str) -> None:
    with sqlite3.connect('peoples.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute("INSERT INTO people_info(date, time, title, name, surname, history) VALUES(?, ?, ?, ?, ?, ?)",
                       (date_now_str, time_now_str, history, name, surname, history))

