import os
import psycopg2
from dotenv import load_dotenv
import asyncpg
import datetime

load_dotenv()

DATABASE = os.getenv('DATABASE_TG')


def connection():
    """
    Connect to the database and return the connection object.

    Returns:
        psycopg2.connection: Connection object if successful, None otherwise
    """
    conn = None
    try:
        conn = psycopg2.connect(DATABASE)
        print('Connection to database established successfully!')
        return conn
    except Exception as e:
        print(f'Failed to connect to database: {e}')
        return None


async def insert_user_name(user_id: int, name: str):
    """
    Add user's name to the database.

    Args:
        user_id (int): Auto incremented user's id.
        name (str): The name entered by the user.

    Returns:
        int: ID of the user who made the message.
    """
    conn = await asyncpg.connect(DATABASE)
    result = await conn.fetchrow('''
        INSERT INTO user_mistakes(user_id, name)
        VALUES ($1, $2)
        RETURNING id''',
                                 user_id, name)
    await conn.close()
    return result['id']


async def insert_mistake(mistake: str, id_: int):
    """
    Сheck the presence of a record at the specified ID.
    If it exists - add the brief statement of the fixed violation
    to the database.

    Args:
        mistake (str): A brief description of the violation
    recorded by the user.
        id_ (int): message ID.
    """
    conn = await asyncpg.connect(DATABASE)
    existing_record = await conn.fetchrow('''
        SELECT *
        FROM user_mistakes
        WHERE id = $1''',
                                          id_)

    if existing_record:
        await conn.execute('''
            UPDATE user_mistakes
            SET mistake = $1
            WHERE id = $2''',
                           mistake, id_)
    else:
        print(f'Запись с id {id_} не найдена. Ошибка не сохранена.')
    await conn.close()


async def insert_description(description: str, id_: int):
    """
    Сheck the presence of a record at the specified ID.
    If it exists - add the detailed description of the fixed violation
    to the database.

    Args:
        description (str): A detailed description of the violation
    recorded by the user.
        id_ (int): message ID.
    """
    conn = await asyncpg.connect(DATABASE)
    existing_record = await conn.fetchrow('''
        SELECT *
        FROM user_mistakes
        WHERE id = $1''',
                                          id_)

    if existing_record:
        await conn.execute('''
        UPDATE user_mistakes
        SET description = $1
        WHERE id = $2''',
                           description, id_)
    else:
        print(f'Запись с id {id_} не найдена. Ошибка не сохранена.')
    await conn.close()


async def insert_level(level: str, id_: int):
    """
    Сheck the presence of a record at the specified ID.
    If it exists - add the importance level of the fixed violation
    to the database.

    Args:
        level (str): A importance level of the violation
    recorded by the user.
        id_ (int): message ID.
    """
    conn = await asyncpg.connect(DATABASE)
    existing_record = await conn.fetchrow('''
        SELECT *
        FROM user_mistakes
        WHERE id = $1''',
                                          id_)

    if existing_record:
        await conn.execute('''
        UPDATE user_mistakes
        SET level = $1
        WHERE id = $2''',
                           level, id_)
    else:
        print(f'Запись с id {id_} не найдена. Ошибка не сохранена.')
    await conn.close()


async def insert_place(place: str, id_: int):
    """
    Сheck the presence of a record at the specified ID.
    If it exists - add the location, premises number where the violation
    was recorded to the database.

    Args:
        place (str): location, premises number where the violation
    was recorded by the user.
        id_ (int): message ID.
    """
    conn = await asyncpg.connect(DATABASE)
    existing_record = await conn.fetchrow('''
        SELECT *
        FROM user_mistakes
        WHERE id = $1''',
                                          id_)

    if existing_record:
        await conn.execute('''
        UPDATE user_mistakes
        SET place = $1
        WHERE id = $2''',
                           place, id_)
    else:
        print(f'Запись с id {id_} не найдена. Ошибка не сохранена.')
    await conn.close()


async def insert_photo(photo_url: str, id_: int):
    """
    Сheck the presence of a record at the specified ID.
    If it exists - add the photo the violation to the database.

    Args:
        photo_url (str): link to photo submitted by user.
        id_ (int): message ID.
    """
    conn = await asyncpg.connect(DATABASE)
    current_time = datetime.datetime.now()
    await conn.execute('''
    UPDATE user_mistakes
    SET photo = $1, 
    timestamp = $2
    WHERE id = $3''',
                       photo_url, current_time, id_)
    await conn.close()
