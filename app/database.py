import aiosqlite
async def init_db():
    async with aiosqlite.connect("job_alert.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_user_id INTEGER NOT NULL,
            query TEXT NOT NULL,
            UNIQUE(telegram_user_id, query)
            )
            """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS sent_vacancies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subscription_id INTEGER NOT NULL,
            vacancy_id TEXT NOT NULL,
            UNIQUE(subscription_id, vacancy_id)
            )
            """)
        await db.commit()
async def add_subscription(telegram_user_id, query):
    async with aiosqlite.connect("job_alert.db") as db:
        cursor = await db.execute("""
            INSERT OR IGNORE INTO subscriptions (
            telegram_user_id,
            query
            )
            VALUES(?,?)
            """, (telegram_user_id, query))
        await db.commit()
        return cursor.rowcount
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
async def was_vacancy_sent(subscription_id, vacancy_id):
    async with aiosqlite.connect("job_alert.db") as db:
        cursor = await db.execute("""
            SELECT 1
            FROM sent_vacancies
            WHERE subscription_id = ?
            AND vacancy_id = ?
            LIMIT 1
            """, (subscription_id, vacancy_id))
        row = await cursor.fetchone()
        return row is not None
async def mark_vacancy_sent(subscription_id, vacancy_id):
    async with aiosqlite.connect("job_alert.db") as db:
        await db.execute("""
            INSERT OR IGNORE INTO sent_vacancies
            (subscription_id, vacancy_id)
            VALUES (?, ?)
        """, (subscription_id, vacancy_id))
        await db.commit()
async def get_all_subscriptions():
    async with aiosqlite.connect("job_alert.db") as db:
        cursor = await db.execute("""
            SELECT id, telegram_user_id, query
            FROM subscriptions
        """)
        rows = await cursor.fetchall()
        return rows