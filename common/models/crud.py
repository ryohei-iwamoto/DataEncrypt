import sqlite3
from .models import *
# DATABASE_PATH = '../../database/app.db'
DATABASE_PATH = './database/app.db'


def create_connection():
    """ データベースへの接続を確立する """
    conn = sqlite3.connect(DATABASE_PATH)
    return conn


def initialize_database():
    """ データベースの初期化とテーブルの作成を行う """
    conn = create_connection()
    cursor = conn.cursor()

    # テーブルとインデックスの作成
    cursor.execute(CREATE_TABLE_SHOPS)
    cursor.execute(CREATE_INDEX_SHOPS_PLACE)
    cursor.execute(CREATE_TABLE_OCCUPANCY_RATES)
    cursor.execute(CREATE_INDEX_OCCUPANCY_WORKING_NUM)
    cursor.execute(CREATE_INDEX_OCCUPANCY_WAITING_NUM)
    cursor.execute(CREATE_TABLE_PREFECTURES)

    conn.commit()
    conn.close()


def create_user(username, email):
    """ 新しいユーザーを作成する """
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email))

    conn.commit()
    conn.close()


def get_prefectures():
    """ 都道府県一覧を取得する """
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT prefecture FROM prefectures")
    prefectures_tuples = cursor.fetchall()

    conn.close()
    prefectures = [prefecture[0] for prefecture in prefectures_tuples]

    return prefectures


def get_user(user_id):
    """ 特定のユーザーを取得する """
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()

    conn.close()
    return user


def update_user(user_id, username, email):
    """ ユーザー情報を更新する """
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET username=?, email=? WHERE id=?", (username, email, user_id))

    conn.commit()
    conn.close()


def delete_user(user_id):
    """ ユーザーを削除する """
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))

    conn.commit()
    conn.close()


initialize_database()