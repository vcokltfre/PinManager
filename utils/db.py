from aiosqlite import connect
from sqlite3 import connect as sync_connect
from pathlib import Path
from asyncio import get_event_loop

DB = "db.sqlite"

CREATE = """CREATE TABLE channels (
    channel INTEGER,
    archive INTEGER,
    PRIMARY KEY (channel)
);
"""

ADD = "INSERT INTO channels (channel, archive) VALUES (?, ?);"
GET = "SELECT archive FROM channels WHERE channel = ?;"
DEL = "DELETE FROM channels WHERE channel = ?;"


class Database:
    def __init__(self):
        if not Path(DB).exists():
            db = sync_connect("db.sqlite")
            db.execute(CREATE)
            db.close()

    async def add_channel(self, channel: int, archive: int):
        async with connect(DB) as db:
            await db.execute_insert(ADD, (channel, archive))
            await db.commit()

    async def get_channel(self, channel: int):
        async with connect(DB) as db:
            async with db.execute(GET, (channel,)) as cur:
                return await cur.fetchone()

    async def remove_channel(self, channel: int):
        async with connect(DB) as db:
            await db.execute_insert(DEL, (channel,))
            await db.commit()
