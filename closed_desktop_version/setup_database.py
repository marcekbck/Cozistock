# database.py
import sqlite3

# Conexão ao banco de dados
conn = sqlite3.connect("products.db")
cursor = conn.cursor()

# Criação da tabela de usuários   /AINDA NAO APLICADA/
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS usuarios (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     nome TEXT NOT NULL,
#     email TEXT NOT NULL UNIQUE,
#     senha TEXT NOT NULL
# )
# """)

# Criação da tabela de produtos
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    expire_date TEXT NOT NULL
    image_path TEXT NOT NULL
)
""")

conn.commit()
conn.close()
