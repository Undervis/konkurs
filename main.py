import random

from fastapi import FastAPI
import sqlite3

sql = sqlite3.connect("jokes.sqlite3")
cursor = sql.cursor()

cursor.execute("create table if not exists Jokes("
               "id integer primary key autoincrement, title varchar(32), content text)")
sql.commit()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Сборник анекдотов про Штирлица"}


@app.get("/joke/{joke_id}")
async def get_joke_by_id(joke_id: int):
    return get_joke(joke_id)


@app.get("/joke")
async def get_rand_joke():
    return get_joke(0)


@app.get("/jokes")
async def get_all_jokes():
    return get_joke(-1)


@app.post("/add_joke")
async def add_joke(title: str, content: str):
    cursor.execute(f'insert into Jokes(title, content) values("{title}", "{content}")')


def get_joke(joke_id=0):
    if joke_id > 0:
        cursor.execute(f"select * from Jokes where id = {joke_id}")
        joke = cursor.fetchone()
        return {"id": joke[0], "title": joke[1], "content": joke[2]}
    elif joke_id == 0:
        cursor.execute(f"select * from Jokes")
        rand_id = random.randrange(1, len(cursor.fetchall()))
        cursor.execute(f"select * from Jokes where id = {rand_id}")
        joke = cursor.fetchone()
        return {"id": joke[0], "title": joke[1], "content": joke[2]}
    elif joke_id == -1:
        cursor.execute(f"select * from Jokes")
        jokes_result = cursor.fetchall()
        return [{"id": joke[0], "title": joke[1], "content": joke[2]} for joke in jokes_result]
