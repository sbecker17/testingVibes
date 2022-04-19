import sqlite3
from sqlite3 import Error
from datetime import date

def create_connection(db_file):
    """ create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)


def close_connection(conn):
    conn.close()

def create_habit_table(conn):
    conn.cursor().execute("""CREATE TABLE if not exists habitlist
                            (
                            username text,
                            category text,
                            name text,
                            count integer,
                            start_date date,
                            last_modified_date date,
                            max_quit_count integer,
                            max_earn_date date
                            )"""
                         )
    conn.commit()

def insert_habit(hab, conn):
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO habitlist(username, category, name, count, start_date, last_modified_date, max_quit_count, max_earn_date) VALUES (:username, :category, :name, :count, :start_date, :last_modified_date, :max_quit_count, :max_earn_date)",
        {'username': hab.username, 'category': hab.category, 'name': hab.name, 'count':hab.count, 'start_date':hab.start_date, 'last_modified_date':hab.last_modified_date, 'max_quit_count':hab.max_quit_count, 'max_earn_date': date.today()})
    conn.commit()

def get_all_habits(conn, username, category):
    c = conn.cursor()
    c.execute("SELECT * FROM habitlist WHERE username =:username AND category =:category", {'username': username, 'category':category})
    return c.fetchall()

def get_habit_by_name(conn, name):
    c = conn.cursor()
    c.execute("SELECT * FROM habitlist WHERE name =:name", {'name': name})
    return c.fetchall()

def get_first_habit(conn):
    conn.cursor().execute("SELECT * FROM habitlist LIMIT 1")
    return conn.cursor().fetchall()

def update_count(count, name, category, conn):
    conn.cursor().execute("UPDATE habitlist SET count = :count WHERE name = :name AND category=:category", {'count': count, 'name': name, 'category':category})
    conn.commit()

def update_max_count(max_quit_count, name, category, conn):
    conn.cursor().execute("UPDATE habitlist SET max_quit_count = :max_quit_count WHERE name = :name AND category=:category", {'max_quit_count': max_quit_count, 'name': name, 'category':category})
    conn.commit()

def update_name(newname, name, conn):
    conn.cursor().execute("UPDATE habitlist SET name = :newname WHERE name = :name", {'newname': newname, 'name': name})
    conn.commit()

def update_last_mod_date(name, conn):
    conn.cursor().execute("UPDATE habitlist SET last_modified_date = :newdate WHERE name = :name", {'newdate': date.today(), 'name': name})
    conn.commit()

def update_max_earn_date(name, conn):
    conn.cursor().execute("UPDATE habitlist SET max_earn_date = :newdate WHERE name = :name", {'newdate': date.today(), 'name': name})
    conn.commit()

def delete_task_db(name, conn):
    conn.cursor().execute("DELETE FROM habitlist WHERE name = :name", {'name': name})
    conn.commit()