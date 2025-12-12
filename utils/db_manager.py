import sqlite3
import os

DB_NAME = 'bot_config.db'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, DB_NAME)
DEFAULT_CONFIG = {
    "auto": False,
    "lang": "es"
}

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS server_configs (
            guild_id TEXT PRIMARY KEY,
            auto_enabled INTEGER DEFAULT 0,
            target_lang TEXT DEFAULT 'es'
        )
    ''')
    conn.commit()
    conn.close()

setup_database()


def get_config(guild_id: int):
    gid = str(guild_id)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT auto_enabled, target_lang FROM server_configs WHERE guild_id = ?', (gid,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return DEFAULT_CONFIG.copy()
    
    return {'auto': bool(row[0]), 'lang': row[1]}


def update_config(guild_id: int, key: str, value):
    gid = str(guild_id)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if key == "auto":
        col_name = "auto_enabled"
        sql_value = 1 if value else 0
    elif key == "lang":
        col_name = "target_lang"
        sql_value = value
    else:
        conn.close()
        raise ValueError(f"Unknown config key: {key}")

    cursor.execute(f'''
        UPDATE server_configs SET {col_name} = ? WHERE guild_id = ?
    ''', (sql_value, gid))
    if cursor.rowcount == 0:
        default = DEFAULT_CONFIG.copy()
        if key == "auto": default["auto"] = value
        if key == "lang": default["lang"] = value

        cursor.execute('''
            INSERT INTO server_configs (guild_id, auto_enabled, target_lang)
            VALUES (?, ?, ?)
        ''', (gid, 1 if default['auto'] else 0, default['lang']))

    conn.commit()
    conn.close()

def set_auto_translate_state(guild_id: int, auto_enabled: bool, target_lang: str):
    gid = str(guild_id)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    auto_val = 1 if auto_enabled else 0
    
    cursor.execute('''
        INSERT OR REPLACE INTO server_configs (guild_id, auto_enabled, target_lang)
        VALUES (?, ?, ?)
    ''', (gid, auto_val, target_lang))
    
    conn.commit()
    conn.close()
