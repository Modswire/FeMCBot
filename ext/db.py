import aiosqlite

async def insert(db, table, variables, contents):
    v = ", ".join(variables)
    c = ", ".join(["?" for i in contents])
    req = f"INSERT INTO {table} ({v}) VALUES ({c});"
    try:
        await db.execute(req, contents)
        await db.commit()
        return True
    except Exception as e:
        return e