"""
Mateus Manoel Encizo Teixeira - UTF8 - ptbr
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from model.mysql_config import mysql  # Importa o objeto mysql para interagir com o banco de dados
from model.rg_model import Registrar
from model.prod_model import Categoria, Produto

# Criação de um Blueprint para o controlador principal
main_bp = Blueprint('main', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa estar logado para acessar esta página!', 'danger')
            return redirect(url_for('main.entrar'))
        return f(*args, **kwargs)
    return decorated_function


# Rota principal (landing)
@main_bp.route('/')
def index():
    # Exibe a página inicial (landing page).
    return render_template('landing.html')

# Rota para a página inicial (home)
@main_bp.route('/home')
def home():
    # Exibe a página principal (home).
    return render_template('home.html')

@main_bp.route('/entrar', methods=['GET', 'POST'])
def entrar():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT id_cliente, senha FROM clientes WHERE email = %s", (email,))
            user = cur.fetchone()
            cur.close()

            if not user:
                flash('E-mail não cadastrado!', 'danger')
                return redirect(url_for('main.entrar'))

            if user[1] == senha:
                session['user_id'] = user[0]  # Armazena o ID do usuário na sessão
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('main.index'))
            else:
                flash('Senha incorreta!', 'danger')
                return redirect(url_for('main.entrar'))

        except Exception as e:
            flash(f"Erro ao acessar o banco de dados: {e}", 'danger')
            return redirect(url_for('main.entrar'))

    return render_template('entrar.html')

@main_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Você saiu da sua conta.', 'success')
    return redirect(url_for('main.index'))

@main_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_usuario():
    return render_template('cadastro.html')

@main_bp.route('/esqueci_senha')
def esqueci_senha():
    return "Página para recuperar senha"

@main_bp.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        nome = request.form['username']
        email = request.form['email']
        senha = request.form['password']
        telefone = request.form['telefone']
        mensagem = Registrar.register(nome, email, senha, telefone) 
        if mensagem == 'success':
            flash(f'Você foi cadastrado com sucesso!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash(f'Falha ao se cadastrar:{mensagem}','danger')
            return redirect(url_for('main.cadastrar_usuario'))

@main_bp.route('/cadastro_categoria', methods=['GET', 'POST'])
@login_required
def cadastro_categorias():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form.get('descricao')
        try:
            nova_categoria = Categoria.cadastrar(nome=nome, descricao=descricao)
            if nova_categoria == 'success':
                flash('Categoria cadastrado com sucesso!', 'success')
            else: 
                flash(f'Ocorreu um erro: {nova_categoria}', 'danger')
            return redirect(url_for('main.cadastro_produto'))
        except Exception as e:
            flash(f'Ocorreu um erro: {e}', 'danger')
            return redirect(url_for('main.cadastro_produto'))
    return render_template('cadastro_categorias.html')


@main_bp.route('/cadastro_produto', methods=['GET', 'POST'])
@login_required
def cadastro_produto():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id_categoria, nome FROM categorias;")
    categorias = cur.fetchall()
    cur.close()
    if request.method == 'POST':
        nome_produto = request.form['nome_produto']
        descricao_produto = request.form['descricao_produto']
        preco_produto = request.form['preco_produto']
        estoque_produto = request.form['estoque_produto']
        categoria_produto = request.form['categoria_produto']
        try:
                novo_produto = Produto.cadastrar(nome_produto, descricao_produto, preco_produto, estoque_produto, categoria_produto)
                if novo_produto == 'success':
                    flash('Produto cadastrado com sucesso!', 'success')
                else:
                    flash(f'Ocorreu um erro: {novo_produto}', 'danger')
                return redirect(url_for('main.cadastro_produto'))
        except Exception as e:
            flash(f'Ocorreu um erro: {e}', 'danger')
            return redirect(url_for('main.cadastro_produto'))
            
    return render_template('cadastro_categorias.html', categorias=categorias)

@main_bp.route('/consulta', methods=['GET','POST'])
@login_required
def consulta():
    views_disponiveis = [
        'listar_pagamentos', 
        'pedidos_pendentes',
        'pedidos_recentes',
        'produtos_por_categoria',
        'produtos_vendidos',
        'total_por_categoria',
        'vm_funcionarios_cargos'
    ]
    
    procedures_disponiveis = {
        'ListarPedidosCliente': ['ID Cliente'],
        'CalcularTotalGastoCliente': ['ID Cliente'],
        'ListarProdutosPorCategoria': ['ID Categoria']
    }

    colunas, resultados, view_selecionada = [], [], None
    procedure_selecionada, procedure_resultado = None, None
    procedure_colunas, procedure_resultados = [], []  # Variáveis separadas para resultados das procedures

    cur = mysql.connection.cursor()

    try:
        if request.method == 'POST':
            if 'consulta_selecionada' in request.form:
                view_selecionada = request.form.get('consulta_selecionada')
                query = f"SELECT * FROM {view_selecionada};"
                cur.execute(query)
                resultados = cur.fetchall()
                colunas = [desc[0] for desc in cur.description]

            elif 'procedure_selecionada' in request.form:
                procedure_selecionada = request.form.get('procedure_selecionada')
                parametro = request.form.get('parametro', '')

                if procedure_selecionada == 'ListarPedidosCliente':
                    cur.callproc('ListarPedidosCliente', [parametro])
                    procedure_resultados = cur.fetchall()
                    procedure_colunas = [desc[0] for desc in cur.description]

                elif procedure_selecionada == 'CalcularTotalGastoCliente':
                    cur.callproc('CalcularTotalGastoCliente', [parametro, 0])
                    cur.execute("SELECT @p_total_gasto")
                    procedure_resultado = cur.fetchone()[0]

                elif procedure_selecionada == 'ListarProdutosPorCategoria':
                    cur.callproc('ListarProdutosPorCategoria', [parametro])
                    procedure_resultados = cur.fetchall()
                    procedure_colunas = [desc[0] for desc in cur.description]
            
        cur.close()

    except Exception as e:
        flash(f'Ocorreu um erro: {e}', 'danger')
        return redirect(url_for('main.consulta'))

    return render_template(
        'consulta.html', 
        views_disponiveis=views_disponiveis,
        colunas=colunas, resultados=resultados, view_selecionada=view_selecionada,
        procedures_disponiveis=procedures_disponiveis, procedure_selecionada=procedure_selecionada,
        procedure_resultado=procedure_resultado,
        procedure_colunas=procedure_colunas, procedure_resultados=procedure_resultados 
    )
