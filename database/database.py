import sqlite3


def init_db():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_mistakes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            mistake TEXT,
            description TEXT,
            level TEXT,
            place TEXT,
            photo BLOB
        )
    ''')

    conn.commit()
    conn.close()


def save_user_data(user_id, name, mistake, description, level, place, photo):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO user_mistakes (user_id, name, mistake, description, level, place, photo)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, name, mistake, description, level, place, photo))

    conn.commit()
    conn.close()


def get_all_mistakes():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM user_mistakes')
    data = cursor.fetchall()

    conn.close()
    return data