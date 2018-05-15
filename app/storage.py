import asyncio
import aiomysql
import os

class MySqlStorage:
    def __init__(self):
        self.pool = None

    async def _get_pool(self):
        if self.pool:
            return self.pool
        (host, port, db) = os.environ['DB_CONN'].split(':')
        self.pool = await aiomysql.create_pool(
            host = host,
            port = int(port),
            user = os.environ['DB_USER'],
            password = os.environ['DB_PASSWORD'],
            db = db,
            loop = asyncio.get_event_loop())
        return self.pool

    async def save_birthday(self, name, date):
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(
                       'REPLACE user (name, birthday) VALUES (%s, %s)',
                       (name, date))
                    await conn.commit()
                except:
                    await conn.rollback()

    async def get_birthday(self, name):
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                rc = await cur.execute('SELECT birthday FROM user WHERE name = %s', name)
                if rc:
                    return (await cur.fetchone())[0]
                else:
                    return None
