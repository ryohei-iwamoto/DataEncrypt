import sqlite3
from .models import *
from datetime import datetime, timedelta
# DATABASE_PATH = '../../database/app.db'
DATABASE_PATH = './database/app.db'

MAX_ATTEMPTS = 8
ATTEMPT_WINDOW = timedelta(minutes=5)


def create_connection():
    """ データベースへの接続を確立する """
    conn = sqlite3.connect(DATABASE_PATH)
    return conn


def initialize_database():
    """ データベースの初期化とテーブルの作成を行う """
    conn = create_connection()
    cursor = conn.cursor()

    # テーブルとインデックスの作成
    cursor.execute(CREATE_TABLE_USERS)
    cursor.execute(CREATE_TABLE_PASSWORDS)
    cursor.execute(CREATE_TABLE_LOGIN_ATTEMPTS)


    conn.commit()
    conn.close()


def check_user(username):
    con = sqlite3.connect(DATABASE_PATH)
    db = con.cursor()
    db.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = db.fetchone()
    con.close()
    return user

def register_user(username, hashed_password):
    # hashed_password = generate_password_hash(password)
    con = sqlite3.connect(DATABASE_PATH)
    db = con.cursor()
    db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hashed_password))
    con.commit()
    con.close()


def record_login_attempt(username):
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    cur.execute("INSERT INTO login_attempts (username, attempt_time) VALUES (?, ?)", (username, datetime.now()))
    con.commit()
    con.close()


def check_login_attempts(username):
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    time_limit = datetime.now() - ATTEMPT_WINDOW
    cur.execute("SELECT COUNT(*) FROM login_attempts WHERE username = ? AND attempt_time > ?", (username, time_limit))
    attempts = cur.fetchone()[0]
    con.close()
    return attempts >= MAX_ATTEMPTS


initialize_database()