import aiosqlite
async def init_db():
    async with aiosqlite.connect("job_alert.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_user_id INTEGER NOT NULL,
            query TEXT NOT NULL
            )
            """)
        await db.commit()
async def add_subscription(telegram_user_id, query):
    async with aiosqlite.connect("job_alert.db") as db:
        await db.execute("""
            INSERT INTO subscriptions (
            telegram_user_id,
            query
            )
            VALUES(?,?)
            """, (telegram_user_id, query))
        await db.commit()
async def get_subscriptions(telegram_user_id):
    async with aiosqlite.connect("job_alert.db") as db:
        cursor = await db.execute("""
            SELECT query
            FROM subscriptions
            WHERE telegram_user_id = ?
            """, (telegram_user_id,))
        rows = await cursor.fetchall()
        return rows
async def delete_subscription(telegram_user_id, query):
    async with aiosqlite.connect("job_alert.db") as db:
        cursor = await db.execute("""
            DELETE FROM subscriptions
            WHERE telegram_user_id = ?
            AND query = ?
            """, (telegram_user_id, query))
        await db.commit()
        return cursor.rowcount