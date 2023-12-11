# models.py


# 会員テーブルの作成
CREATE_TABLE_USERS = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    email TEXT,
    hash TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    status TEXT
);
"""

# パスワード管理テーブルの作成
CREATE_TABLE_PASSWORDS = """
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY,
    member_id INTEGER,
    file_name TEXT,
    password TEXT,
    created_at TIMESTAMP,
    memo TEXT,
    FOREIGN KEY (member_id) REFERENCES members (id)
);
"""


CREATE_TABLE_LOGIN_ATTEMPTS = """
    CREATE TABLE IF NOT EXISTS login_attempts (
        id INTEGER PRIMARY KEY,
        username TEXT,
        attempt_time TIMESTAMP
    );
"""