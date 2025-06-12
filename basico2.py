"""
Mateus Manoel Encizo Teixeira - ptbr - basico2.py
"""

from flask import Flask
from flask_mysqldb import MySQL
from model.mysql_config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

if __name__ == "__main__":
    with app.app_context():
        try:
            print("Conectando ao banco de dados...")
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM usuarios;")
            users = cur.fetchall()
            cur.close()
            print(f"Usuários encontrados: {users}")
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

