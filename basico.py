"""
Mateus Manoel Encizo Teixeira - ptbr
basico.py
"""

from flask import Flask
from flask_mysqldb import MySQL

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Configuração do MySQL
app.config["MYSQL_HOST"] = "localhost"          # Host do banco de dados
app.config["MYSQL_USER"] = "root"              # Usuário do MySQL
app.config["MYSQL_PASSWORD"] = "alunoifro"    # Senha do MySQL que você utilizou
app.config["MYSQL_DB"] = "supermercado"           # Nome do seu banco de dados

# Inicializa a extensão MySQL
mysql = MySQL(app)

# Teste direto no script, sem a necessidade de rotas
if __name__ == "__main__":
    with app.app_context():  # Cria um contexto de aplicação
        try:
            # Tenta conectar ao banco de dados e executar uma consulta
            print("Conectando ao banco de dados...")
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM clientes;")  # Substitua pela sua tabela
            users = cur.fetchall()
            cur.close()
            print(f"Usuários encontrados: {users}")  # Exibe os usuários retornados
        except Exception as e:
            # Captura e exibe qualquer erro ocorrido
            print(f"Erro ao conectar ao banco de dados: {e}")

    # Inicia o servidor Flask (opcional para uso futuro)
    app.run(debug=True)
