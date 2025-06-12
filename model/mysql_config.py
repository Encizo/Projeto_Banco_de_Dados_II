"""
Mateus Manoel Encizo Teixeira - UTF8 - ptbr - mysql_config.py
"""

from flask_mysqldb import MySQL
import os

# Classe para armazenar configurações da aplicação
class Config:
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DB = os.getenv("MYSQL_DB", "")
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24))

# Objeto MySQL
mysql = MySQL()

# Inicializa o MySQL com as configurações do app Flask
def init_mysql(app):
    mysql.init_app(app)

