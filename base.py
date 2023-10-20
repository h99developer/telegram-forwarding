import aiosqlite

async def Connect():
    db = await aiosqlite.connect('base.db')
    sql = await db.cursor()

    return db, sql

async def createTables():
    db, sql = await Connect()

    await sql.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER,
        first_name TEXT,
        thread_id INTEGER
    )""")

    await db.commit()
    await db.close()

async def isExist(user_id: int) -> bool:
    db, sql = await Connect()

    await sql.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    result = await sql.fetchone()

    await db.close()

    if result == None:
        return False
    else:
        return True
    

async def insertUser(user_id: int, first_name: int, thread_id: int) -> bool:
    db, sql = await Connect()

    await sql.execute("INSERT INTO users VALUES (?, ?, ?)", (user_id, first_name, thread_id,))
    
    await db.commit()
    await db.close()

async def getThread(user_id: int) -> int:
    db, sql = await Connect()

    await sql.execute("SELECT thread_id FROM users WHERE user_id = ?", (user_id,))
    result = await sql.fetchone()

    await db.commit()
    await db.close()

    return int(result[0])

async def getUserFromThreadId(thread_id : int) -> int:
    db, sql = await Connect()

    await sql.execute("SELECT user_id FROM users WHERE thread_id = ?", (thread_id,))
    result = await sql.fetchone()

    await db.close()

    return int(result[0])

async def getAllUsers() -> list:
    db, sql = await Connect()

    await sql.execute("SELECT * FROM users")
    result = await sql.fetchall()

    await db.close()

    return result