# models.py


# shops テーブルの作成
CREATE_TABLE_SHOPS = """
CREATE TABLE IF NOT EXISTS shops (
    id INTEGER PRIMARY KEY,
    name TEXT,
    prefecture TEXT,
    url TEXT NOT NULL,
    business_hours TEXT,
    cost TEXT,
    place TEXT,
    review_num TEXT,
    shop_catch TEXT,
    shop_text TEXT,
    create_date TIMESTAMP,
    update_date TIMESTAMP
);
"""

# shops テーブルの place カラムにインデックスを作成
CREATE_INDEX_SHOPS_PLACE = "CREATE INDEX IF NOT EXISTS idx_shops_place ON shops (place);"

# occupancy_rate テーブルの作成
CREATE_TABLE_OCCUPANCY_RATES = """
CREATE TABLE IF NOT EXISTS occupancy_rates (
    id INTEGER PRIMARY KEY,
    shop_id INTEGER NOT NULL,
    rate REAL,
    working_num INTEGER,
    waiting_num INTEGER,
    FOREIGN KEY (shop_id) REFERENCES shops(id)
);
"""

# occupancy_rate テーブルの working_num と waiting_num カラムにインデックスを作成
CREATE_INDEX_OCCUPANCY_WORKING_NUM = "CREATE INDEX IF NOT EXISTS idx_occupancy_working_num ON occupancy_rates (working_num);"
CREATE_INDEX_OCCUPANCY_WAITING_NUM = "CREATE INDEX IF NOT EXISTS idx_occupancy_waiting_num ON occupancy_rates (waiting_num);"


# prefectureのテーブル作成
CREATE_TABLE_PREFECTURES = """
CREATE TABLE IF NOT EXISTS prefectures (
    id INTEGER PRIMARY KEY,
    prefecture TEXT,
    create_date TIMESTAMP,
    update_date TIMESTAMP
);
"""
