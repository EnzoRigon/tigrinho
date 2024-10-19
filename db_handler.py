import sqlite3


def connect_db():
    conn = sqlite3.connect('tigrinho.db')
    return conn


def add_user(user):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO people (user, balance) VALUES (?, ?)
    ''', (user, 100.0))
    conn.commit()
    conn.close()


def get_people():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM people')
    people = cursor.fetchall()
    conn.close()
    return people


def alter_balance(user, balance):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE people SET balance = ? WHERE user = ?
    ''', (balance, user))
    conn.commit()
    conn.close()


def check_or_add_user(user):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT balance FROM people WHERE user = ?', (user,))
    result = cursor.fetchone()
    
    if result:
        balance = result[0]
        conn.close()
        return user, balance
    else:
        add_user(user)
        conn.close()
        return user, 100.0


def get_ranking():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT user, balance FROM people ORDER BY balance DESC')
    results = cursor.fetchall()

    conn.close()
    return results


def get_balance(user):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT balance FROM people WHERE user = ?', (user,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]
    else:
        return None
