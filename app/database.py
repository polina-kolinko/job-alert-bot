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