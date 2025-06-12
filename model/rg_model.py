"""
Mateus Manoel Encizo Teixeira - UTF8 - ptbr - rg_model.py
"""

from model.mysql_config import mysql

class Registrar:
    @staticmethod
    def register(nome, email, senha, telefone):
        try:
            cur = mysql.connection.cursor()
            cur.callproc('CadastrarCliente', (nome, email, senha, telefone))
            mysql.connection.commit()
            cur.close()
            return 'success'
        except Exception as e:
            return str(e)