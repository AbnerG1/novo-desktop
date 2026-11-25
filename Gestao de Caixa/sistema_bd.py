# import sqlite3

# class BancoDeDados:
#     def __init__(self):
#         self.nome_banco = "sistema_caixa.db"
#         self.inicializar_banco()

#     def inicializar_banco(self):
#         con = sqlite3.connect(self.nome_banco)
#         cur = con.cursor()
#         # ID do produto agora é AUTOINCREMENT (Gera sozinho)
#         cur.execute('''CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, preco REAL, quantidade INTEGER)''')
#         cur.execute('''CREATE TABLE IF NOT EXISTS vendas (id INTEGER PRIMARY KEY AUTOINCREMENT, total REAL)''')
#         cur.execute('''CREATE TABLE IF NOT EXISTS itens_venda (id INTEGER PRIMARY KEY AUTOINCREMENT, venda_id INTEGER, produto_nome TEXT, quantidade INTEGER, subtotal REAL)''')
#         con.commit()
#         con.close()

# class EstoqueBD(BancoDeDados):
#     # O método cadastrar não pede mais o id_p!
#     def cadastrar(self, nome, preco, qtd):
#         try:
#             con = sqlite3.connect(self.nome_banco)
#             cur = con.cursor()
#             cur.execute("INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)", (nome, preco, qtd))
#             id_gerado = cur.lastrowid # Captura o ID que o banco gerou sozinho
#             con.commit()
#             con.close()
#             return True, f"Produto cadastrado com sucesso! ID gerado: {id_gerado:02d}"
#         except Exception as e:
#             return False, f"Erro ao cadastrar: {e}"

#     def listar_produtos(self):
#         con = sqlite3.connect(self.nome_banco)
#         cur = con.cursor()
#         cur.execute("SELECT id, nome, preco, quantidade FROM produtos")
#         produtos = cur.fetchall()
#         con.close()
#         return produtos

#     def atualizar(self, id_p, preco, qtd):
#         con = sqlite3.connect(self.nome_banco)
#         cur = con.cursor()
#         cur.execute("UPDATE produtos SET preco = ?, quantidade = ? WHERE id = ?", (preco, qtd, id_p))
#         sucesso = cur.rowcount > 0
#         con.commit()
#         con.close()
#         return sucesso

#     def deletar(self, id_p):
#         con = sqlite3.connect(self.nome_banco)
#         cur = con.cursor()
#         cur.execute("DELETE FROM produtos WHERE id = ?", (id_p,))
#         sucesso = cur.rowcount > 0
#         con.commit()
#         con.close()
#         return sucesso

#     def buscar_produto(self, id_p):
#         con = sqlite3.connect(self.nome_banco)
#         cur = con.cursor()
#         cur.execute("SELECT id, nome, preco, quantidade FROM produtos WHERE id = ?", (id_p,))
#         produto = cur.fetchone()
#         con.close()
#         return produto  

# class VendasBD(BancoDeDados):
#     def obter_proximo_id(self):
#         con = sqlite3.connect(self.nome_banco)
#         cur = con.cursor()
#         cur.execute("SELECT MAX(id) FROM vendas")
#         resultado = cur.fetchone()[0]
#         con.close()
#         return 1 if resultado is None else resultado + 1

#     def registrar_venda_e_baixar_estoque(self, total, carrinho):
#         con = sqlite3.connect(self.nome_banco)
#         cur = con.cursor()
#         cur.execute("INSERT INTO vendas (total) VALUES (?)", (total,))
#         id_venda = cur.lastrowid
        
#         for item in carrinho:
#             cur.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?", (item['qtd'], item['id']))
#             cur.execute("INSERT INTO itens_venda (venda_id, produto_nome, quantidade, subtotal) VALUES (?, ?, ?, ?)",
#                         (id_venda, item['nome'], item['qtd'], item['subtotal']))
                        
#         con.commit()
#         con.close()
#         return id_venda

#     def relatorio_dia(self):
#         con = sqlite3.connect(self.nome_banco)
#         cur = con.cursor()
#         cur.execute("SELECT id, total FROM vendas")
#         vendas = cur.fetchall()
#         con.close()
#         return vendas


import sqlite3

class BancoDeDados:
    """Classe base que gerencia a conexão e criação do banco."""
    def __init__(self):
        self.nome_banco = "sistema_caixa.db"
        self.inicializar_banco()

    def inicializar_banco(self):
        con = sqlite3.connect(self.nome_banco)
        cur = con.cursor()
        # Adicionado AUTOINCREMENT no ID do produto para gerar automaticamente (1, 2, 3...)
        cur.execute('''CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, preco REAL, quantidade INTEGER)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS vendas (id INTEGER PRIMARY KEY AUTOINCREMENT, total REAL)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS itens_venda (id INTEGER PRIMARY KEY AUTOINCREMENT, venda_id INTEGER, produto_nome TEXT, quantidade INTEGER, subtotal REAL)''')
        con.commit()
        con.close()

class EstoqueBD(BancoDeDados):
    """Classe que herda BancoDeDados para gerenciar o CRUD de Produtos."""
    
    # Removido o parâmetro id_p, pois agora o banco gera sozinho
    def cadastrar(self, nome, preco, qtd):
        try:
            con = sqlite3.connect(self.nome_banco)
            cur = con.cursor()
            cur.execute("INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)", (nome, preco, qtd))
            con.commit()
            con.close()
            return True, "Produto cadastrado com sucesso!"
        except Exception as e:
            return False, f"Erro ao cadastrar: {e}"

    def listar_produtos(self):
        con = sqlite3.connect(self.nome_banco)
        cur = con.cursor()
        cur.execute("SELECT id, nome, preco, quantidade FROM produtos")
        produtos = cur.fetchall()
        con.close()
        return produtos

    def atualizar(self, id_p, preco, qtd):
        con = sqlite3.connect(self.nome_banco)
        cur = con.cursor()
        cur.execute("UPDATE produtos SET preco = ?, quantidade = ? WHERE id = ?", (preco, qtd, id_p))
        sucesso = cur.rowcount > 0
        con.commit()
        con.close()
        return sucesso

    def deletar(self, id_p):
        con = sqlite3.connect(self.nome_banco)
        cur = con.cursor()
        cur.execute("DELETE FROM produtos WHERE id = ?", (id_p,))
        sucesso = cur.rowcount > 0
        con.commit()
        con.close()
        return sucesso

    def buscar_produto(self, id_p):
        con = sqlite3.connect(self.nome_banco)
        cur = con.cursor()
        cur.execute("SELECT id, nome, preco, quantidade FROM produtos WHERE id = ?", (id_p,))
        produto = cur.fetchone()
        con.close()
        return produto  

class VendasBD(BancoDeDados):
    """Classe que herda BancoDeDados para gerenciar transações financeiras."""
    def obter_proximo_id(self):
        con = sqlite3.connect(self.nome_banco)
        cur = con.cursor()
        cur.execute("SELECT MAX(id) FROM vendas")
        resultado = cur.fetchone()[0]
        con.close()
        return 1 if resultado is None else resultado + 1

    def registrar_venda_e_baixar_estoque(self, total, carrinho):
        con = sqlite3.connect(self.nome_banco)
        cur = con.cursor()
        
        cur.execute("INSERT INTO vendas (total) VALUES (?)", (total,))
        id_venda = cur.lastrowid
        
        for item in carrinho:
            cur.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?", (item['qtd'], item['id']))
            cur.execute("INSERT INTO itens_venda (venda_id, produto_nome, quantidade, subtotal) VALUES (?, ?, ?, ?)",
                        (id_venda, item['nome'], item['qtd'], item['subtotal']))
                        
        con.commit()
        con.close()
        return id_venda

    def relatorio_dia(self):
        con = sqlite3.connect(self.nome_banco)
        cur = con.cursor()
        cur.execute("SELECT id, total FROM vendas")
        vendas = cur.fetchall()
        con.close()
        return vendas