import os
import psycopg2
from dotenv import load_dotenv
import asyncpg
import asyncio

load_dotenv()

DATABASE = os.getenv('DATABASE_TG')


def connection():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE)
        print('Connection to database established successfully!')
        return conn
    except Exception as e:
        print(f'Failed to connect to database: {e}')
        return None


async def insert_user_name(user_id: int, name:str):
    conn = await asyncpg.connect(DATABASE)
    # await conn.execute('''
    result = await conn.fetchrow('''
        INSERT INTO user_mistakes(user_id, name)
        VALUES ($1, $2)
        RETURNING id''',
                       user_id, name)
    await conn.close()
    return result['id']

async def insert_mistake(mistake: str, id: int):
    conn = await asyncpg.connect(DATABASE)
    existing_record = await conn.fetchrow('SELECT * FROM user_mistakes WHERE id = $1', id)

    if existing_record:
        await conn.execute('''
            UPDATE user_mistakes
            SET mistake = $1
            WHERE id = $2''',
                           mistake, id)
    else:
        print(f'Запись с id {id} не найдена. Ошибка не сохранена.')
    await conn.close()

async def insert_description(description: str, id: int):
    conn = await asyncpg.connect(DATABASE)
    existing_record = await conn.fetchrow('SELECT * FROM user_mistakes WHERE id = $1', id)

    if existing_record:
        await conn.execute('''
        UPDATE user_mistakes
        SET description = $1
        WHERE id = $2''',
                           description, id)
    else:
        print(f'Запись с id {id} не найдена. Ошибка не сохранена.')
    await conn.close()

async def insert_level(level: str, id: int):
    conn = await asyncpg.connect(DATABASE)
    existing_record = await conn.fetchrow('SELECT * FROM user_mistakes WHERE id = $1', id)

    if existing_record:
        await conn.execute('''
        UPDATE user_mistakes
        SET level = $1
        WHERE id = $2''',
                           level, id)
    else:
        print(f'Запись с id {id} не найдена. Ошибка не сохранена.')
    await conn.close()

async def insert_place(place: str, id: int):
    conn = await asyncpg.connect(DATABASE)
    existing_record = await conn.fetchrow('SELECT * FROM user_mistakes WHERE id = $1', id)

    if existing_record:
        await conn.execute('''
        UPDATE user_mistakes
        SET place = $1
        WHERE id = $2''',
                           place, id)
    else:
        print(f'Запись с id {id} не найдена. Ошибка не сохранена.')
    await conn.close()
