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


def get_manage_passwords(user_id):
    # ユーザーIDに基づいてパスワード情報を取得
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    cur.execute("SELECT id, file_name, password, created_at, memo FROM passwords WHERE member_id = ?", (user_id,))
    passwords_raw = cur.fetchall()
    con.close()

    passwords = []
    for password in passwords_raw:
        id, file_name, password, created_at, memo = password
        date_only = created_at.split(' ')[0]  # 半角スペースで分割し、最初の要素を取得
        passwords.append((id, file_name, password, date_only, memo))

    return passwords


def delete_manage_password(password_id):
    # パスワード情報の削除
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    cur.execute("DELETE FROM passwords WHERE id = ?", (password_id,))
    con.commit()
    con.close()


def save_password(user_id, key, file_name):
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    cur.execute("INSERT INTO passwords (member_id, file_name, password, memo, created_at) VALUES (?, ?, ?, ?, ?)", (user_id, file_name, key, '', datetime.now()))
    con.commit()
    con.close()


def change_password_memo(password_id, memo):
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    cur.execute("UPDATE passwords SET memo = ? WHERE id = ?;", (memo, password_id))
    con.commit()
    con.close()



initialize_database()