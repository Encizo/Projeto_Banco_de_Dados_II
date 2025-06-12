from model.mysql_config import mysql

class Categoria():
    def cadastrar(nome, descricao):
        try:
            cur = mysql.connection.cursor()
            cur.callproc("InserirCategoria", (nome, descricao))
            mysql.connection.commit()
            cur.close()
            return 'success'
        except Exception as e:
            return e

class Produto():
    def cadastrar(nome, descricao, preco, estoque, categoria_id):
        try:
            cur = mysql.connection.cursor()
            cur.callproc("InserirProduto", (nome, descricao, preco, estoque, categoria_id))
            mysql.connection.commit()
            cur.close()
            return 'success'
        except Exception as e:
            return e