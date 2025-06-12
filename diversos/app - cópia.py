
"""
Mateus Manoel Encizo Teixeira - UTF8 - ptbr
"""
from flask import Flask, redirect, url_for, render_template
from controller.main_controller import main_bp

app = Flask(__name__)

# Registro do Blueprint para o controlador principal
app.register_blueprint(main_bp)

# Definir a rota principal como ponto de entrada redirecionando para /landing
@app.route('/')
def index():
    return redirect(url_for('main.landing'))

@app.route("/entrar")
def entrar():
    return render_template("entrar.html")

if __name__ == '__main__':
    app.run(debug=True)

