import tkinter as tk
from tkinter import simpledialog, messagebox
from sistema_bd import EstoqueBD, VendasBD

# Paleta de Cores Global
BG_SISTEMA = "#121214"
BG_OPCOES = "#202024"
COR_TITULO = "#FFFFFF"
COR_SUBTITULO = "#A8A8B3"
COR_BORDA = "#323238"
COR_DESTAQUE_VERDE = "#04D361"
COR_DESTAQUE_LARANJA = "#EF760B"
COR_PERIGO_VERMELHO = "#A60000"

class GestaoCaixaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Gestão de Caixa - PDV (Nível 4)")
        self.geometry("1920x1080")
        self.configure(bg=BG_SISTEMA)
        self.state('zoomed') 
        
        self.estoque_db = EstoqueBD()
        self.vendas_db = VendasBD()
        
        self.perfil_atual = None
        self.carrinho = []
        self.total_venda = 0.0
        
        self.container = tk.Frame(self, bg=BG_SISTEMA)
        self.container.pack(fill="both", expand=True)
        
        self.frames = {}
        for F in (LoginFrame, AdminFrame, FuncionarioFrame, VendaFrame):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
            
        self.mostrar_frame(LoginFrame)

    def mostrar_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()
        if frame_class == VendaFrame:
            frame.preparar_nova_venda()

# Adicionado o parâmetro cor_texto para permitir alterar a cor da fonte facilmente
def criar_botao(parent, texto, cor_fundo, comando, largura=35, cor_texto=COR_TITULO):
    """Função auxiliar para padronizar os botões com a borda solicitada"""
    frame_borda = tk.Frame(parent, bg=COR_BORDA, padx=2, pady=2)
    btn = tk.Button(frame_borda, text=texto, font=("Arial", 14, "bold"), bg=cor_fundo, fg=cor_texto, 
                    width=largura, height=2, relief="flat", activebackground=cor_fundo, activeforeground=cor_texto, command=comando)
    btn.pack(fill="both", expand=True)
    return frame_borda

# --- TELA 1: LOGIN ---
class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_SISTEMA)
        self.controller = controller
        
        # Painel centralizado
        painel = tk.Frame(self, bg=BG_OPCOES, highlightbackground=COR_BORDA, highlightthickness=2)
        painel.place(relx=0.5, rely=0.5, anchor="center", width=600, height=450)
        
        tk.Label(painel, text="SELECIONE SEU ACESSO", font=("Arial", 26, "bold"), bg=BG_OPCOES, fg=COR_TITULO).pack(pady=(50, 10))
        tk.Label(painel, text="Escolha seu perfil para iniciar o sistema", font=("Arial", 12), bg=BG_OPCOES, fg=COR_SUBTITULO).pack(pady=(0, 40))
        
        criar_botao(painel, "ADMINISTRADOR / GERENTE", COR_DESTAQUE_LARANJA, self.acesso_admin).pack(pady=15)
        criar_botao(painel, "FUNCIONÁRIO (CAIXA)", COR_DESTAQUE_VERDE, self.acesso_funcionario).pack(pady=15)

    def acesso_admin(self):
        senha = simpledialog.askstring("Segurança", "Digite a senha (Admin):", show='*')
        if senha == "1234":
            self.controller.perfil_atual = "Admin"
            self.controller.mostrar_frame(AdminFrame)
        else:
            if senha is not None:
                messagebox.showerror("Erro", "Senha Incorreta!")

    def acesso_funcionario(self):
        self.controller.perfil_atual = "Funcionario"
        self.controller.mostrar_frame(FuncionarioFrame)

# --- TELA 2: ADMIN (CRUD COMPLETO COM LISTAGEM) ---
class AdminFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_SISTEMA)
        self.controller = controller
        
        painel = tk.Frame(self, bg=BG_OPCOES, highlightbackground=COR_BORDA, highlightthickness=2)
        painel.place(relx=0.5, rely=0.5, anchor="center", width=700, height=850)
        
        tk.Label(painel, text="PAINEL ADMINISTRATIVO", font=("Arial", 26, "bold"), bg=BG_OPCOES, fg=COR_DESTAQUE_LARANJA).pack(pady=(40, 10))
        tk.Label(painel, text="Gerenciamento de Estoque e Relatórios", font=("Arial", 12), bg=BG_OPCOES, fg=COR_SUBTITULO).pack(pady=(0, 30))
        
        criar_botao(painel, "1. Criar Produto", BG_SISTEMA, self.criar).pack(pady=10)
        criar_botao(painel, "2. Listar Produtos em Estoque", BG_SISTEMA, self.listar).pack(pady=10)
        criar_botao(painel, "3. Atualizar Produto", BG_SISTEMA, self.atualizar).pack(pady=10)
        
        # Ajuste: Fundo padrão do sistema, mas letras na cor VERMELHA
        criar_botao(painel, "4. Deletar Produto", BG_SISTEMA, self.deletar, cor_texto=COR_PERIGO_VERMELHO).pack(pady=10)
        
        criar_botao(painel, "5. Relatório de Vendas do Dia", BG_SISTEMA, self.relatorio).pack(pady=10)
        
        tk.Label(painel, text="", bg=BG_OPCOES).pack(pady=5) # Espaçador
        
        criar_botao(painel, "INICIAR NOVA VENDA (Admin)", COR_DESTAQUE_LARANJA, lambda: controller.mostrar_frame(VendaFrame)).pack(pady=15)
        
        # Ajuste: Removido o argumento 'largura=25', agora o botão assume o tamanho padrão de 35
        criar_botao(painel, "SAIR (Trocar Usuário)", COR_PERIGO_VERMELHO, lambda: controller.mostrar_frame(LoginFrame)).pack(pady=15)

    def criar(self):
        nome = simpledialog.askstring("Novo", "Nome do Produto:")
        if not nome: return
        preco = simpledialog.askfloat("Novo", "Preço (R$):")
        if preco is None: return
        qtd = simpledialog.askinteger("Novo", "Quantidade em Estoque:")
        if qtd is None: return
        
        sucesso, msg = self.controller.estoque_db.cadastrar(nome, preco, qtd)
        if sucesso: messagebox.showinfo("OK", msg)
        else: messagebox.showerror("Erro", msg)

    def listar(self):
        produtos = self.controller.estoque_db.listar_produtos()
        if not produtos:
            messagebox.showinfo("Estoque", "O estoque está vazio.")
            return
            
        texto = "=== PRODUTOS NO ESTOQUE ===\n\n"
        for p in produtos:
            texto += f"ID: {p[0]:02d} | {p[1]} | R$ {p[2]:.2f} | Estoque: {p[3]} un\n"
        messagebox.showinfo("Listagem de Estoque", texto)

    def atualizar(self):
        id_p = simpledialog.askinteger("Update", "ID do Produto:")
        if id_p:
            preco = simpledialog.askfloat("Update", "Novo Preço (R$):")
            qtd = simpledialog.askinteger("Update", "Nova Quantidade:")
            if self.controller.estoque_db.atualizar(id_p, preco, qtd):
                messagebox.showinfo("OK", "Atualizado com sucesso!")
            else:
                messagebox.showwarning("Erro", "Produto não encontrado.")

    def deletar(self):
        id_p = simpledialog.askinteger("Deletar", "ID do Produto:")
        if id_p:
            if self.controller.estoque_db.deletar(id_p): messagebox.showinfo("OK", "Deletado!")
            else: messagebox.showwarning("Erro", "Produto não encontrado.")

    def relatorio(self):
        vendas = self.controller.vendas_db.relatorio_dia()
        texto = "=== FECHAMENTO DO DIA ===\n\n"
        total_geral = 0
        for v in vendas:
            texto += f"Venda ID #{v[0]:02d}: R$ {v[1]:.2f}\n"
            total_geral += v[1]
        texto += f"\nTOTAL EM CAIXA: R$ {total_geral:.2f}"
        messagebox.showinfo("Relatório", texto)

# --- TELA 3: FUNCIONÁRIO ---
class FuncionarioFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_SISTEMA)
        self.controller = controller
        
        painel = tk.Frame(self, bg=BG_OPCOES, highlightbackground=COR_BORDA, highlightthickness=2)
        painel.place(relx=0.5, rely=0.5, anchor="center", width=600, height=450)
        
        tk.Label(painel, text="ÁREA DO FUNCIONÁRIO", font=("Arial", 26, "bold"), bg=BG_OPCOES, fg=COR_DESTAQUE_VERDE).pack(pady=(60, 10))
        tk.Label(painel, text="Terminal de Caixa", font=("Arial", 12), bg=BG_OPCOES, fg=COR_SUBTITULO).pack(pady=(0, 40))
        
        criar_botao(painel, "INICIAR NOVA VENDA", COR_DESTAQUE_VERDE, lambda: controller.mostrar_frame(VendaFrame)).pack(pady=20)
        criar_botao(painel, "SAIR", COR_PERIGO_VERMELHO, lambda: controller.mostrar_frame(LoginFrame), largura=20).pack(pady=20)

# --- TELA 4: VENDA ---
class VendaFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_SISTEMA)
        self.controller = controller
        
        painel = tk.Frame(self, bg=BG_OPCOES, highlightbackground=COR_BORDA, highlightthickness=2)
        painel.place(relx=0.5, rely=0.5, anchor="center", width=1000, height=800)
        
        self.lbl_titulo = tk.Label(painel, text="VENDA #00", font=("Arial", 28, "bold"), bg=BG_OPCOES, fg=COR_TITULO)
        self.lbl_titulo.pack(pady=(30, 5))
        tk.Label(painel, text="Detalhes do Carrinho", font=("Arial", 12), bg=BG_OPCOES, fg=COR_SUBTITULO).pack(pady=(0, 20))
        
        frame_lista = tk.Frame(painel, bg=COR_BORDA, padx=2, pady=2)
        frame_lista.pack(pady=10)
        self.lista = tk.Listbox(frame_lista, font=("Courier", 16), width=70, height=14, bg=BG_SISTEMA, fg=COR_TITULO, relief="flat", highlightthickness=0)
        self.lista.pack()
        
        self.lbl_total = tk.Label(painel, text="TOTAL: R$ 0.00", font=("Arial", 26, "bold"), bg=BG_OPCOES, fg=COR_DESTAQUE_VERDE)
        self.lbl_total.pack(pady=25)
        
        frame_b = tk.Frame(painel, bg=BG_OPCOES)
        frame_b.pack(pady=10)
        
        criar_botao(frame_b, "Adicionar Produto", BG_SISTEMA, self.add_produto, largura=20).grid(row=0, column=0, padx=15)
        criar_botao(frame_b, "FECHAR VENDA", COR_DESTAQUE_VERDE, self.fechar_venda, largura=20).grid(row=0, column=1, padx=15)
        criar_botao(frame_b, "CANCELAR VENDA", COR_PERIGO_VERMELHO, self.cancelar_venda, largura=20).grid(row=0, column=2, padx=15)

    def preparar_nova_venda(self):
        self.controller.carrinho = []
        self.controller.total_venda = 0.0
        prox_id = self.controller.vendas_db.obter_proximo_id()
        self.lbl_titulo.config(text=f"NOVA VENDA #{prox_id:02d}")
        self.atualizar_visor()

    def atualizar_visor(self):
        self.lista.delete(0, tk.END)
        for item in self.controller.carrinho:
            self.lista.insert(tk.END, f"{item['nome']:<25} | Qtd: {item['qtd']:<3} | Subtotal: R$ {item['subtotal']:.2f}")
        self.lbl_total.config(text=f"TOTAL: R$ {self.controller.total_venda:.2f}")

    def add_produto(self):
        id_p = simpledialog.askinteger("Add", "ID do Produto:")
        if not id_p: return
        qtd = simpledialog.askinteger("Add", "Quantidade desejada:")
        if not qtd: return
        
        produto = self.controller.estoque_db.buscar_produto(id_p)
        if not produto:
            messagebox.showerror("Erro", "Produto não encontrado!")
            return
            
        qtd_ja_carrinho = sum(i['qtd'] for i in self.controller.carrinho if i['id'] == id_p)
        estoque_real = produto[3]
        
        if (qtd + qtd_ja_carrinho) > estoque_real:
            messagebox.showerror("Estoque Insuficiente", f"Você só possui {estoque_real} itens desse no banco.")
            return
            
        subtotal = produto[2] * qtd
        self.controller.carrinho.append({"id": id_p, "nome": produto[1], "preco": produto[2], "qtd": qtd, "subtotal": subtotal})
        self.controller.total_venda += subtotal
        self.atualizar_visor()

    def fechar_venda(self):
        if not self.controller.carrinho:
            messagebox.showwarning("Vazio", "Nenhum produto adicionado.")
            return
            
        id_gerado = self.controller.vendas_db.registrar_venda_e_baixar_estoque(self.controller.total_venda, self.controller.carrinho)
        messagebox.showinfo("Sucesso", f"Venda #{id_gerado:02d} fechada com sucesso!\nTotal: R$ {self.controller.total_venda:.2f}")
        self.encerrar_ciclo()

    def cancelar_venda(self):
        if self.controller.perfil_atual == "Funcionario":
            senha = simpledialog.askstring("Autorização Admin", "Digite a senha do ADMIN para cancelar a venda:", show='*')
            if senha != "1234":
                messagebox.showerror("Erro", "Senha Inválida! Venda NÃO cancelada.")
                return
        
        messagebox.showinfo("Cancelado", "Venda Cancelada. Nenhum produto foi retirado do estoque.")
        self.encerrar_ciclo()

    def encerrar_ciclo(self):
        if self.controller.perfil_atual == "Admin":
            self.controller.mostrar_frame(AdminFrame)
        else:
            self.controller.mostrar_frame(FuncionarioFrame)

if __name__ == "__main__":
    app = GestaoCaixaApp()
    app.mainloop()
