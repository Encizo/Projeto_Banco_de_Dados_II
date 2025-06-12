"""
USE supermercado;

DELIMITER $$

CREATE PROCEDURE CadastrarCliente(
    IN p_nome VARCHAR(100),
    IN p_email VARCHAR(100),
    IN p_senha VARCHAR(255),
    IN p_telefone VARCHAR(20)
)
BEGIN
    INSERT INTO clientes (nome, email, senha, telefone)
    VALUES (p_nome, p_email, p_senha, p_telefone);
END $$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE InserirProduto(
    IN p_nome VARCHAR(100),
    IN p_descricao TEXT,
    IN p_preco DECIMAL(10,2),
    IN p_estoque INT,
    IN p_id_categoria INT
)
BEGIN
    INSERT INTO produtos (nome, descricao, preco, estoque, id_categoria)
    VALUES (p_nome, p_descricao, p_preco, p_estoque, p_id_categoria);
END $$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE CadastrarPedido(
    IN p_id_cliente INT,
    IN p_status VARCHAR(50)
)
BEGIN
    INSERT INTO pedidos (id_cliente, status)
    VALUES (p_id_cliente, p_status);
END $$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE AtualizarStatusPedido(
    IN p_id_pedido INT,
    IN p_status VARCHAR(50)
)
BEGIN
    UPDATE pedidos
    SET status = p_status
    WHERE id_pedido = p_id_pedido;
END $$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE RegistrarPagamento(
    IN p_id_pedido INT,
    IN p_tipo VARCHAR(50),
    IN p_valor DECIMAL(10,2)
)
BEGIN
    INSERT INTO pagamentos (id_pedido, tipo, valor)
    VALUES (p_id_pedido, p_tipo, p_valor);
END $$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE InserirItemPedido(
    IN p_id_pedido INT,
    IN p_id_produto INT,
    IN p_quantidade INT,
    IN p_preco DECIMAL(10,2)
)
BEGIN
    INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco)
    VALUES (p_id_pedido, p_id_produto, p_quantidade, p_preco);
END $$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE ListarPedidosCliente(
    IN p_id_cliente INT
)
BEGIN
    SELECT *
    FROM pedidos
    WHERE id_cliente = p_id_cliente;
END $$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE CalcularTotalGastoCliente(
    IN p_id_cliente INT,
    OUT p_total_gasto DECIMAL(10,2)
)
BEGIN
    SELECT SUM(p.valor) INTO p_total_gasto
    FROM pagamentos p
    JOIN pedidos pd ON p.id_pedido = pd.id_pedido
    WHERE pd.id_cliente = p_id_cliente AND pd.status = 'concluído';
END $$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE AtualizarEstoqueProduto(
    IN p_id_produto INT,
    IN p_quantidade INT
)
BEGIN
    UPDATE produtos
    SET estoque = estoque - p_quantidade
    WHERE id_produto = p_id_produto;
END $$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE ListarProdutosPorCategoria(
    IN p_id_categoria INT
)
BEGIN
    SELECT *
    FROM produtos
    WHERE id_categoria = p_id_categoria;
END $$

DELIMITER ;

CREATE PROCEDURE InserirCategoria(
    IN p_nome VARCHAR(100),
    IN p_descricao TEXT
)
BEGIN
    INSERT INTO categorias (nome, descricao) 
    VALUES (p_nome, p_descricao);
END $$

DELIMITER ;
"""