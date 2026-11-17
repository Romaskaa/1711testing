from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from db import init_db, query


app = FastAPI()
init_db()


class ClubInput(BaseModel):
    name: str


@app.get("/api/clubs")
def get_clubs():
    return query("SELECT * FROM clubs ORDER BY id", many=True)


@app.get("/api/rooms")
def get_rooms():
    return query("SELECT * FROM rooms ORDER BY id", many=True)


@app.post("/api/clubs")
def add_club(club: ClubInput):
    return query("INSERT INTO clubs (name) VALUES (%s) RETURNING *", (club.name,))


@app.put("/api/clubs/{club_id}")
def update_club(club_id: int, club: ClubInput):
    result = query(
        "UPDATE clubs SET name = %s WHERE id = %s RETURNING *",
        (club.name, club_id),
    )
    if result is None:
        raise HTTPException(404, "Клуб не найден")
    return result


@app.delete("/api/clubs/{club_id}")
def delete_club(club_id: int):
    result = query("DELETE FROM clubs WHERE id = %s RETURNING *", (club_id,))
    if result is None:
        raise HTTPException(404, "Клуб не найден")
    return result
