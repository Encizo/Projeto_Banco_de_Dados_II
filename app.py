"""
Mateus Manoel Encizo Teixeira- UTF8 - ptbr
"""
from flask import Flask
from model.mysql_config import Config, init_mysql
from controller.main_controller import main_bp

# Configuração inicial
app = Flask(__name__)

# Carrega as configurações do arquivo mysql_config.py
app.config.from_object(Config)  

init_mysql(app)  # Inicializa o MySQL

# Registro do blueprint principal
app.register_blueprint(main_bp)


if __name__ == '__main__':
    app.run(debug=True)
