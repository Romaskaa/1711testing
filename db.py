import os

import psycopg
from psycopg.rows import dict_row


DATABASE_URL = os.getenv("DATABASE_URL")

CLUBS = {
    1: {"id": 1, "name": "IT-клуб"},
    2: {"id": 2, "name": "Шахматный клуб"},
    3: {"id": 3, "name": "Киноклуб"},
}

ROOMS = {
    1: {"id": 1, "name": "Ауд. 214", "building": "Главный корпус", "capacity": 40},
    2: {"id": 2, "name": "Ауд. 101", "building": "Главный корпус", "capacity": 120},
    3: {"id": 3, "name": "Коворкинг", "building": "Научная библиотека", "capacity": 25},
}


def query(sql, params=(), many=False):
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as db:
        result = db.execute(sql, params)
        if result.description:
            return result.fetchall() if many else result.fetchone()


def init_db():
    with psycopg.connect(DATABASE_URL) as db:
        clubs_new = db.execute("SELECT to_regclass('public.clubs') IS NULL").fetchone()[0]
        rooms_new = db.execute("SELECT to_regclass('public.rooms') IS NULL").fetchone()[0]

        db.execute("CREATE TABLE IF NOT EXISTS clubs (id SERIAL PRIMARY KEY, name TEXT NOT NULL)")
        db.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                building TEXT NOT NULL,
                capacity INTEGER NOT NULL
            )
        """)

        if clubs_new:
            for club in CLUBS.values():
                db.execute("INSERT INTO clubs (name) VALUES (%s)", (club["name"],))

        if rooms_new:
            for room in ROOMS.values():
                db.execute(
                    "INSERT INTO rooms (name, building, capacity) VALUES (%s, %s, %s)",
                    (room["name"], room["building"], room["capacity"]),
                )
