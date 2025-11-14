import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk, ImageDraw
import os
import customtkinter as ctk
import requests
import uuid


API_URL = "http://127.0.0.1:8000"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


USUARIO_LOGADO = None

COR_FUNDO = "#003366"
COR_CAIXA = "#2c2c2c"

def aplicar_fundo_azul(imagem):
    imagem = imagem.convert("RGBA")
    fundo = Image.new("RGBA", imagem.size, (0, 51, 102, 255))  # RGB azul escuro
    fundo.paste(imagem, (0, 0), imagem)
    return fundo

def fale_conosco(janela_atual=None):
    janela = ctk.CTk()
    janela.title("Chat Simples")
    janela.geometry("500x400")
    janela.configure(fg_color=COR_FUNDO)

    label = ctk.CTkLabel(janela, text="Digite sua mensagem:", fg_color=COR_FUNDO)
    label.pack(pady=10)

    entrada = ctk.CTkEntry(janela, width=400, fg_color=COR_CAIXA, placeholder_text="Escreva algo...")
    entrada.pack(pady=10)

    botao = ctk.CTkButton(janela, text="Enviar", command=cadastrar_aluno)
    botao.pack(pady=10)

    caixa_resposta = ctk.CTkTextbox(janela, width=450, height=200, fg_color=COR_CAIXA)
    caixa_resposta.pack(pady=10)
    caixa_resposta.configure(state="disabled") 

    janela.mainloop()

def cadastrar_professor(janela_atual=None):
    if janela_atual:
        janela_atual.destroy()

    janela = ctk.CTkToplevel()
    janela.title("Cadastro de Professor")
    janela.geometry("600x700")
    janela.configure(fg_color=COR_FUNDO)
    janela.resizable(False, False)

    titulo = ctk.CTkLabel(
        janela,
        text="Cadastro de Professor",
        font=("Arial", 28, "bold"),
        text_color="white"
    )
    titulo.pack(pady=30)

    ctk.CTkLabel(janela, text="Nome:", font=("Arial", 20), text_color="white").pack(pady=(10, 0))
    entry_nome = ctk.CTkEntry(janela, width=400, height=50, font=("Arial", 18))
    entry_nome.pack(pady=5)

    ctk.CTkLabel(janela, text="E-mail:", font=("Arial", 20), text_color="white").pack(pady=(10, 0))
    entry_email = ctk.CTkEntry(janela, width=400, height=50, font=("Arial", 18))
    entry_email.pack(pady=5)

    ctk.CTkLabel(janela, text="Senha:", font=("Arial", 20), text_color="white").pack(pady=(10, 0))
    entry_senha = ctk.CTkEntry(janela, width=400, height=50, font=("Arial", 18), show="*")
    entry_senha.pack(pady=5)

    def salvar_professor():
        nome = entry_nome.get().strip()
        email = entry_email.get().strip()
        senha = entry_senha.get().strip()

        if not nome or not email or not senha:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
            return

        try:
            resposta = requests.post(
                f"{API_URL}/cadastro/professor",
                json={"nome": nome, "email": email, "senha": senha}
            )

            if resposta.status_code == 200:
                messagebox.showinfo("Sucesso", "Professor cadastrado com sucesso!")
                janela.destroy()
            else:
                erro = resposta.json().get("detail", "Erro desconhecido.")
                messagebox.showerror("Erro", f"Falha ao cadastrar: {erro}")

        except requests.exceptions.ConnectionError:
            messagebox.showerror("Erro", "Não foi possível conectar ao servidor API.\nVerifique se ele está rodando.")

    ctk.CTkButton(
        janela,
        text="Cadastrar",
        width=300,
        height=60,
        corner_radius=30,
        font=("Arial", 20, "bold"),
        command=salvar_professor
    ).pack(pady=30)

    ctk.CTkButton(
        janela,
        text="Cancelar",
        width=300,
        height=60,
        corner_radius=30,
        font=("Arial", 20, "bold"),
        command=janela.destroy
    ).pack()
    
def tentar_login(email_entry, senha_entry, janela_login):
    global USUARIO_LOGADO

    email = email_entry.get().strip()
    senha = senha_entry.get().strip()

    if not email or not senha:
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    try:
        resposta = requests.post(f"{API_URL}/login", json={"nome": "", "email": email, "senha": senha})

        if resposta.status_code == 200:
            dados_login = resposta.json()
            USUARIO_LOGADO = dados_login["usuario"]

            tipo_usuario = dados_login["tipo"]
            nome_usuario = USUARIO_LOGADO["nome"]

            messagebox.showinfo("Sucesso", f"Bem-vindo, {nome_usuario}!")

            janela_login.destroy()

            if tipo_usuario == "professor":
                menu_professor()
            else:
                menu_aluno()

        else:
            erro = resposta.json().get("detail", "Credenciais inválidas.")
            messagebox.showerror("Erro", erro)

    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "Não foi possível conectar à API.\nVerifique se o servidor está rodando.")

def logar_professor(janela_atual=None):
    if janela_atual:
        janela_atual.destroy()

    janela_login = ctk.CTkToplevel()
    janela_login.title("Área do Login")
    janela_login.geometry("1360x768")
    janela_login.configure(fg_color=COR_FUNDO)

    ctk.CTkLabel(
        janela_login,
        text="Por favor, faça seu login!",
        font=("Arial", 28, "bold"),
        text_color="white"
    ).place(relx=0.5, y=100, anchor="center")

    ctk.CTkLabel(
        janela_login,
        text="E-mail:",
        font=("Arial", 22),
        text_color="white"
    ).place(relx=0.5, y=200, anchor="center")
    email_entry = ctk.CTkEntry(janela_login, font=("Arial", 22), width=400, height=50)
    email_entry.place(relx=0.5, y=240, anchor="center")

    ctk.CTkLabel(
        janela_login,
        text="Senha:",
        font=("Arial", 22),
        text_color="white"
    ).place(relx=0.5, y=300, anchor="center")
    senha_entry = ctk.CTkEntry(janela_login, font=("Arial", 22), width=400, height=50, show="*")
    senha_entry.place(relx=0.5, y=340, anchor="center")

    def realizar_login():
        email = email_entry.get().strip()
        senha = senha_entry.get().strip()

        if not email or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        try:
            resposta = requests.post(f"{API_URL}/login", json={"nome": "", "email": email, "senha": senha})

            if resposta.status_code == 200:
                dados_login = resposta.json()
                global USUARIO_LOGADO
                USUARIO_LOGADO = dados_login["usuario"]

                tipo_usuario = dados_login["tipo"]
                nome_usuario = USUARIO_LOGADO["nome"]

                messagebox.showinfo("Sucesso", f"Bem-vindo, {nome_usuario}!")
                janela_login.destroy()

                if tipo_usuario == "professor":
                    menu_professor()
                else:
                    menu_aluno()

            else:
                erro = resposta.json().get("detail", "Credenciais inválidas.")
                messagebox.showerror("Erro", erro)

        except requests.exceptions.ConnectionError:
            messagebox.showerror("Erro", "Não foi possível conectar à API.\nVerifique se o servidor está rodando.")

    ctk.CTkButton(
        janela_login,
        text="Login",
        width=300,
        height=60,
        corner_radius=30,
        font=("Arial", 22, "bold"),
        command=realizar_login
    ).place(relx=0.5, y=420, anchor="center")

    ctk.CTkButton(
        janela_login,
        text="Cancelar",
        width=300,
        height=60,
        corner_radius=30,
        font=("Arial", 22, "bold"),
        command=janela_login.destroy
    ).place(relx=0.5, y=500, anchor="center")

def gerenciar_turmas(botao=None):
    if botao:
        janela_atual = botao.winfo_toplevel()
        janela_atual.destroy()
    
    janela_menu = tk.Toplevel()
    janela_menu.title("Gerenciar Turmas")
    janela_menu.geometry("1360x768")
    janela_menu.configure(bg=COR_FUNDO)

    tk.Label(
        janela_menu,
        text="Gerenciar Turmas",
        font=("Arial", 28, "bold"),
        bg=COR_FUNDO,
        fg="white"
    ).pack(pady=20)

    ctk.CTkButton(
        janela_menu,
        text="1 - Ver Turmas",
        width=400,
        height=60,
        corner_radius=30,
        font=("Arial", 20, "bold"),
        command=lambda: ver_turmas(janela_menu)
    ).pack(pady=10)

    # ---------- Botão Cadastrar Nova Turma ----------
    ctk.CTkButton(
        janela_menu,
        text="2 - Cadastrar Nova Turma",
        width=400,
        height=60,
        corner_radius=30,
        font=("Arial", 20, "bold"),
        command=lambda: cadastrar_turmas(janela_menu)
    ).pack(pady=10)

    ctk.CTkButton(
        janela_menu,
        text="3 - Alterar Turma",
        width=400,
        height=60,
        corner_radius=30,
        font=("Arial", 20, "bold"),
        command=lambda: alterar_turmas(janela_menu)
    ).pack(pady=10)

    ctk.CTkButton(
        janela_menu,
        text="4 - Excluir Turma",
        width=400,
        height=60,
        corner_radius=30,
        font=("Arial", 20, "bold"),
        command=lambda: excluir_turma(janela_menu)
    ).pack(pady=10)

    ctk.CTkButton(
        janela_menu,
        text="5 - Voltar",
        width=400,
        height=60,
        corner_radius=30,
        font=("Arial", 20, "bold"),
        command=janela_menu.destroy
    ).pack(pady=10)

def aluno():
    janela.withdraw()
    janela_aluno = tk.Toplevel()
    janela_aluno.title("Área do Aluno")
    janela_aluno.geometry("1360x768")
    janela_aluno.configure(bg=COR_FUNDO)

    ctk.CTkLabel(
        janela_aluno,
        text="Bem-vindo, Aluno!",
        font=("Arial", 28, "bold"),
        text_color="white"
    ).pack(pady=40)

    ctk.CTkButton(
        janela_aluno,
        text="Logar",
        width=400,
        height=70,
        corner_radius=35,
        fg_color=None,
        hover_color=None,
        text_color="white",
        font=("Arial", 24, "bold"),
        command=lambda: [janela_aluno.destroy(), logar_aluno()]
    ).pack(pady=10)

    ctk.CTkButton(
        janela_aluno,
        text="Cadastrar",
        width=400,
        height=70,
        corner_radius=35,
        fg_color=None,
        hover_color=None,
        text_color="white",
        font=("Arial", 24, "bold"),
        command=cadastrar_aluno
    ).pack(pady=10)

    ctk.CTkButton(
        janela_aluno,
        text="Voltar",
        width=400,
        height=70,
        corner_radius=35,
        fg_color=None,
        hover_color=None,
        text_color="white",
        font=("Arial", 24, "bold"),
        command=lambda: voltar_para_menu(janela_aluno)
    ).pack(pady=10)

def cadastrar_aluno(janela_atual=None):
    if janela_atual:
        janela_atual.destroy()

    janela_cadastro = tk.Toplevel()
    janela_cadastro.title("Cadastro de Aluno")
    janela_cadastro.geometry("600x700")
    janela_cadastro.configure(bg=COR_FUNDO)

    ctk.CTkLabel(
        janela_cadastro,
        text="Cadastro de Aluno",
        font=("Arial", 28, "bold"),
        text_color="white"
    ).pack(pady=30)

    ctk.CTkLabel(janela_cadastro, text="Nome:", font=("Arial", 20), text_color="white").pack(pady=(10, 0))
    entry_nome = ctk.CTkEntry(janela_cadastro, width=400, height=50, font=("Arial", 18))
    entry_nome.pack(pady=5)

    ctk.CTkLabel(janela_cadastro, text="E-mail:", font=("Arial", 20), text_color="white").pack(pady=(10, 0))
    entry_email = ctk.CTkEntry(janela_cadastro, width=400, height=50, font=("Arial", 18))
    entry_email.pack(pady=5)

    ctk.CTkLabel(janela_cadastro, text="Senha:", font=("Arial", 20), text_color="white").pack(pady=(10, 0))
    entry_senha = ctk.CTkEntry(janela_cadastro, width=400, height=50, font=("Arial", 18), show="*")
    entry_senha.pack(pady=5)

    def salvar_aluno():
        nome = entry_nome.get().strip()
        email = entry_email.get().strip()
        senha = entry_senha.get().strip()

        if not nome or not email or not senha:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
            return

        try:
            resposta = requests.post(
                f"{API_URL}/cadastro/aluno",
                json={"nome": nome, "email": email, "senha": senha}
            )

            if resposta.status_code == 200:
                messagebox.showinfo("Sucesso", f"Aluno {nome} cadastrado com sucesso!")
                janela_cadastro.destroy()
            else:
                erro = resposta.json().get("detail", "Erro desconhecido.")
                messagebox.showerror("Erro", erro)

        except requests.exceptions.ConnectionError:
            messagebox.showerror("Erro", "Não foi possível conectar à API.\nVerifique se o servidor está rodando.")

    ctk.CTkButton(
        janela_cadastro,
        text="Cadastrar",
        width=300,
        height=60,
        corner_radius=30,
        font=("Arial", 20, "bold"),
        command=salvar_aluno
    ).pack(pady=30)

    ctk.CTkButton(
        janela_cadastro,
        text="Cancelar",
        width=300,
        height=60,
        corner_radius=30,
        font=("Arial", 20, "bold"),
        command=janela_cadastro.destroy
    ).pack()

def logar_aluno(janela_anterior=None):
    if janela_anterior:
        janela_anterior.destroy()

    janela_login = tk.Toplevel()
    janela_login.title("Área do Login")
    janela_login.geometry("600x500")
    janela_login.configure(bg=COR_FUNDO)

    ctk.CTkLabel(janela_login, text="Por favor, faça seu login!",
                 font=("Arial", 28, "bold"), text_color="white").pack(pady=30)

    ctk.CTkLabel(janela_login, text="E-mail:", font=("Arial", 22), text_color="white").pack(pady=5)
    email_entry = ctk.CTkEntry(janela_login, font=("Arial", 22), width=400)
    email_entry.pack(pady=5)

    ctk.CTkLabel(janela_login, text="Senha:", font=("Arial", 22), text_color="white").pack(pady=5)
    senha_entry = ctk.CTkEntry(janela_login, font=("Arial", 22), width=400, show="*")
    senha_entry.pack(pady=5)

    def login():
        global USUARIO_LOGADO
        email = email_entry.get().strip()
        senha = senha_entry.get().strip()

        if not email or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        try:
            resposta = requests.post(
                f"{API_URL}/login",
                json={"email": email, "senha": senha}  # Apenas email e senha
            )

            if resposta.status_code == 200:
                dados_login = resposta.json()
                USUARIO_LOGADO = dados_login["usuario"]
                messagebox.showinfo("Sucesso", f"Bem-vindo, {USUARIO_LOGADO.get('nome', 'Aluno')}!")
                janela_login.destroy()
                menu_aluno()
            else:
                erro = resposta.json().get("detail", "Credenciais inválidas.")
                messagebox.showerror("Erro", erro)

        except requests.exceptions.ConnectionError:
            messagebox.showerror("Erro", "Não foi possível conectar à API.\nVerifique se o servidor está rodando.")

    ctk.CTkButton(janela_login, text="Login", width=300, height=60, corner_radius=30,
                  font=("Arial", 22, "bold"), command=login).pack(pady=20)

    ctk.CTkButton(janela_login, text="Cancelar", width=300, height=60, corner_radius=30,
                  font=("Arial", 22, "bold"), command=janela_login.destroy).pack(pady=10)

def menu_aluno(janela_anterior=None):
    global USUARIO_LOGADO

    if janela_anterior:
        janela_anterior.destroy()

    janela = ctk.CTk()
    janela.title("Menu do Aluno")
    janela.geometry("1360x768")
    janela.configure(fg_color=COR_FUNDO)

    titulo = ctk.CTkLabel(
        janela,
        text=f"Menu do Aluno ({USUARIO_LOGADO['nome']})",
        font=("Arial", 20, "bold"),
        text_color="white"
    )
    titulo.pack(pady=20)

    botoes = [
        ("Ver turmas", ver_turmas),
        ("Ver notas", ver_resultados),
        ("Ver atividades", listar_atividades_para_responder),
        ("Ver Perfil", ver_perfil), 
        ("Sair da conta", lambda: sair_conta(janela)),
    ]

    for texto, comando in botoes:
        botao = ctk.CTkButton(
            janela,
            text=texto,
            width=400,
            height=70,
            font=("Arial", 14),
            command=comando
        )
        botao.pack(pady=10)

    janela.mainloop()

def sair_conta(janela):
    global USUARIO_LOGADO
    resposta = messagebox.askyesno("Sair", "Deseja realmente sair da conta?")
    if resposta:
        USUARIO_LOGADO = None
        messagebox.showinfo("Logout", "Você saiu da conta.")
        janela.destroy()

def listar_turmas(janela_anterior=None):
    if janela_anterior:
        janela_anterior.destroy()

    janela_turmas = ctk.CTk()
    janela_turmas.title("Turmas Disponíveis")
    janela_turmas.geometry("600x400")
    janela_turmas.configure(fg_color=COR_FUNDO)

    titulo = ctk.CTkLabel(
        janela_turmas,
        text="Turmas Disponíveis",
        font=("Arial", 22, "bold"),
        text_color="white"
    )
    titulo.pack(pady=20)

    try:
        resposta = requests.get(f"{API_URL}/turmas")
        if resposta.status_code == 200:
            turmas = resposta.json()
        else:
            messagebox.showerror("Erro", "Falha ao buscar turmas.")
            turmas = []
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "Não foi possível conectar à API.")
        turmas = []

    if not turmas:
        mensagem = ctk.CTkLabel(
            janela_turmas,
            text="Nenhuma turma cadastrada.",
            font=("Arial", 16),
            text_color="white"
        )
        mensagem.pack(pady=10)
    else:
        frame_scroll = ctk.CTkScrollableFrame(janela_turmas, width=500, height=250)
        frame_scroll.pack(pady=10)

        for i, turma in enumerate(turmas, 1):
            texto = f"{i}. {turma['nome']} - Professor: {turma.get('professor', 'N/A')}"
            label = ctk.CTkLabel(
                frame_scroll,
                text=texto,
                font=("Arial", 16),
                text_color="white",
                anchor="w"
            )
            label.pack(fill="x", pady=3)

    ctk.CTkButton(
        janela_turmas,
        text="Voltar",
        width=200,
        height=40,
        font=("Arial", 14),
        command=lambda: voltar_menu(janela_turmas)
    ).pack(pady=20)

    janela_turmas.mainloop()

def voltar_menu(janela):
    janela.destroy()
    menu_aluno()

def ver_perfil(janela_principal=None):
    global USUARIO_LOGADO

    # Use Toplevel se já existir janela principal
    janela = ctk.CTkToplevel(janela_principal) if janela_principal else ctk.CTk()
    janela.title("Perfil do Usuário")
    janela.geometry("500x400")
    janela.configure(fg_color=COR_FUNDO)

    ctk.CTkLabel(
        janela,
        text="Meu Perfil",
        font=("Arial", 24, "bold"),
        text_color="white"
    ).pack(pady=20)

    ctk.CTkLabel(janela, text=f"Nome: {USUARIO_LOGADO['nome']}", font=("Arial", 16), text_color="white").pack(pady=5)
    ctk.CTkLabel(janela, text=f"Email: {USUARIO_LOGADO['email']}", font=("Arial", 16), text_color="white").pack(pady=5)

    # Função para editar perfil
    def editar_perfil():
        editar_janela = ctk.CTkToplevel(janela)
        editar_janela.title("Editar Perfil")
        editar_janela.geometry("400x300")
        editar_janela.configure(fg_color=COR_FUNDO)

        ctk.CTkLabel(editar_janela, text="Editar Perfil", font=("Arial", 20, "bold"), text_color="white").pack(pady=10)

        nome_entry = ctk.CTkEntry(editar_janela, placeholder_text="Novo nome", width=300)
        nome_entry.insert(0, USUARIO_LOGADO["nome"])
        nome_entry.pack(pady=5)

        email_entry = ctk.CTkEntry(editar_janela, placeholder_text="Novo email", width=300)
        email_entry.insert(0, USUARIO_LOGADO["email"])
        email_entry.pack(pady=5)

        senha_entry = ctk.CTkEntry(editar_janela, placeholder_text="Nova senha", show="*", width=300)
        senha_entry.insert(0, USUARIO_LOGADO["senha"])
        senha_entry.pack(pady=5)

        def salvar_edicao():
            novo_nome = nome_entry.get().strip()
            novo_email = email_entry.get().strip()
            nova_senha = senha_entry.get().strip()

            try:
                resposta = requests.put(
                    f"{API_URL}/editar/usuario",
                    json={
                        "email": USUARIO_LOGADO["email"],
                        "nome": novo_nome,
                        "senha": nova_senha,
                        "novo_email": novo_email
                    }
                )
                if resposta.status_code == 200:
                    USUARIO_LOGADO.update({"nome": novo_nome, "email": novo_email, "senha": nova_senha})
                    messagebox.showinfo("Sucesso", "Perfil atualizado com sucesso!")
                    editar_janela.destroy()
                    janela.destroy()
                    ver_perfil(janela_principal)
                else:
                    erro = resposta.json().get("detail", "Erro ao atualizar perfil.")
                    messagebox.showerror("Erro", erro)
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Erro", "Não foi possível conectar à API.")

        ctk.CTkButton(editar_janela, text="Salvar Alterações", width=200, height=40, command=salvar_edicao).pack(pady=15)

    # Função para excluir perfil
    def excluir_perfil():
        global USUARIO_LOGADO
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir o perfil?"):
            try:
                r = requests.delete(f"{API_URL}/excluir/usuario", json={"email": USUARIO_LOGADO["email"]})
                if r.status_code == 200:
                    USUARIO_LOGADO = None
                    messagebox.showinfo("Conta excluída", "Seu perfil foi removido com sucesso!")
                    janela.destroy()
                else:
                    erro = r.json().get("detail", "Erro ao excluir perfil.")
                    messagebox.showerror("Erro", erro)
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Erro", "Não foi possível conectar à API.")

    ctk.CTkButton(janela, text="Editar Perfil", width=200, height=40, command=editar_perfil).pack(pady=10)
    ctk.CTkButton(janela, text="Excluir Perfil", width=200, height=40, fg_color="red", command=excluir_perfil).pack(pady=10)
    ctk.CTkButton(janela, text="Fechar", width=200, height=40, command=janela.destroy).pack(pady=10)

    if not janela_principal:
        janela.mainloop()

def responder_atividade(atividade, janela_origem=None):
    if janela_origem:
        janela_origem.after(120, janela_origem.destroy)

    janela = ctk.CTk()
    janela.title("Responder Atividade")
    janela.geometry("700x480")
    janela.configure(fg_color=COR_FUNDO)

    ctk.CTkLabel(janela, text=f"Turma: {atividade.get('turma','Geral')}",
                 font=("Arial", 18, "bold"), text_color="white").pack(pady=(12,6))

    ctk.CTkLabel(janela, text=atividade.get("pergunta", ""),
                 font=("Arial", 16), text_color="white", wraplength=640, justify="left").pack(pady=(0,18))

    resposta_var = ctk.StringVar(value="")
    alternativas = atividade.get("alternativas", {})

    for letra in ["A", "B", "C", "D"]:
        texto = alternativas.get(letra, "")
        if texto:
            ctk.CTkRadioButton(
                janela,
                text=f"{letra}) {texto}",
                variable=resposta_var,
                value=letra,
                font=("Arial", 14),
                text_color="white"
            ).pack(anchor="w", padx=40, pady=6)

    def enviar():
        escolha = resposta_var.get()
        if not escolha:
            messagebox.showwarning("Aviso", "Selecione uma alternativa!")
            return

        try:
            payload = {
                "usuario_email": USUARIO_LOGADO["email"],
                "atividade_id": atividade.get("id"),
                "resposta": escolha
            }
            r = requests.post(f"{API_URL}/responder_atividade", json=payload)
            if r.status_code == 200:
                resultado = r.json().get("resultado", "")
                messagebox.showinfo("Resultado", resultado)
            else:
                erro = r.json().get("detail", "Erro ao enviar resposta.")
                messagebox.showerror("Erro", erro)
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Erro", "Não foi possível conectar à API.")

        janela.after(120, janela.destroy)

    ctk.CTkButton(janela, text="Enviar Resposta", width=220, height=48,
                  command=enviar, font=("Arial", 14, "bold")).pack(pady=20)

    ctk.CTkButton(janela, text="Voltar", width=160, height=40,
                  command=lambda: janela.after(80, janela.destroy)).pack(pady=(0,8))

    janela.mainloop()

def listar_atividades_para_responder(janela_anterior=None):
    if janela_anterior:
        janela_anterior.after(120, janela_anterior.destroy)

    try:
        r = requests.get(f"{API_URL}/atividades")
        if r.status_code == 200:
            atividades = r.json()
        else:
            messagebox.showerror("Erro", "Falha ao buscar atividades.")
            atividades = []
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "Não foi possível conectar à API.")
        atividades = []

    janela = ctk.CTk()
    janela.title("Atividades (Geral)")
    janela.geometry("820x620")
    janela.configure(fg_color=COR_FUNDO)

    ctk.CTkLabel(janela, text="Atividades Disponíveis (Geral)",
                 font=("Arial", 24, "bold"), text_color="white").pack(pady=16)

    if not atividades:
        ctk.CTkLabel(janela, text="Nenhuma atividade cadastrada.", font=("Arial", 16), text_color="white").pack(pady=20)
        ctk.CTkButton(janela, text="Voltar", width=200, command=lambda: janela.after(80, janela.destroy)).pack(pady=10)
        janela.mainloop()
        return

    frame = ctk.CTkScrollableFrame(janela, width=760, height=440)
    frame.pack(pady=10, padx=20)

    for i, atv in enumerate(atividades, start=1):
        texto = f"{i}. ({atv.get('turma','Geral')}) {atv.get('pergunta','')}"
        
        def abrir(a=atv, win=janela):
            responder_atividade(a, janela_origem=win)
        
        ctk.CTkButton(frame, text=texto, width=720, height=50, anchor="w",
                      command=abrir, font=("Arial", 13)).pack(pady=6)

    ctk.CTkButton(janela, text="Voltar", width=200, command=lambda: janela.after(80, janela.destroy)).pack(pady=12)
    janela.mainloop()

def ver_resultados(janela_anterior=None):
    if janela_anterior:
        janela_anterior.after(120, janela_anterior.destroy)

    try:
        r = requests.get(f"{API_URL}/notas", params={"email": USUARIO_LOGADO["email"]})
        if r.status_code == 200:
            dados_notas = r.json()
            np1 = dados_notas.get("np1", 0)
            np2 = dados_notas.get("np2", 0)
        else:
            messagebox.showerror("Erro", "Falha ao obter notas.")
            np1 = np2 = 0
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "Não foi possível conectar à API.")
        np1 = np2 = 0

    media = (np1 + np2) / 2
    status = "Aprovado ✅" if media >= 6 else "Reprovado ❌"

    janela = ctk.CTk()
    janela.title("Notas do Aluno")
    janela.geometry("500x350")
    janela.configure(fg_color=COR_FUNDO)

    ctk.CTkLabel(janela, text="Notas do Aluno", font=("Arial", 26, "bold"), text_color="white").pack(pady=20)

    frame = ctk.CTkFrame(janela, fg_color="#2c2c2c", corner_radius=12)
    frame.pack(padx=20, pady=20, fill="x")

    ctk.CTkLabel(frame, text=f"NP1: {np1}", font=("Arial", 20), text_color="white").pack(pady=10)
    ctk.CTkLabel(frame, text=f"NP2: {np2}", font=("Arial", 20), text_color="white").pack(pady=10)
    ctk.CTkLabel(frame, text=f"Média Final: {media:.1f}", font=("Arial", 20, "bold"),
                  text_color="lightgreen" if media >= 6 else "red").pack(pady=10)
    ctk.CTkLabel(frame, text=f"Situação: {status}", font=("Arial", 18),
                  text_color="lightgreen" if media >= 6 else "red").pack(pady=5)

    ctk.CTkButton(janela, text="Fechar", width=200, height=40, font=("Arial", 14),
                  command=janela.destroy).pack(pady=20)

    janela.mainloop()

def menu_professor():

    janela_menu = tk.Toplevel()
    janela_menu.title("Menu do Professor")
    janela_menu.geometry("1360x768")
    janela_menu.configure(bg=COR_FUNDO)

    tk.Label(janela_menu, text="O que deseja fazer?", font=("Arial", 24, "bold"),
             bg=COR_FUNDO, fg="white").pack(pady=30)

    ctk.CTkButton(
        janela_menu, text="Gerenciar Turmas", width=400, height=60, corner_radius=30,
        font=("Arial", 20, "bold"), fg_color=None, hover_color=None, text_color="white",
        command=gerenciar_turmas
    ).pack(pady=10)

    ctk.CTkButton(
        janela_menu, text="Gerenciar Alunos", width=400, height=60, corner_radius=30,
        font=("Arial", 20, "bold"), fg_color=None, hover_color=None, text_color="white",
        command=gerenciar_alunos_gui
    ).pack(pady=10)

    ctk.CTkButton(
        janela_menu, text="Editar Perfil", width=400, height=60, corner_radius=30,
        font=("Arial", 20, "bold"), fg_color=None, hover_color=None, text_color="white",
        command=perfil_professor_gui
    ).pack(pady=10)

    ctk.CTkButton(
        janela_menu, text="Gerenciar Atividades", width=400, height=60, corner_radius=30,
        font=("Arial", 20, "bold"), fg_color=None, hover_color=None, text_color="white",
        command=gerenciar_atividades
    ).pack(pady=10)

    def deslogar():
        janela_menu.destroy() 
        janela.deiconify()


    ctk.CTkButton(
    janela_menu, text="Sair", width=400, height=60, corner_radius=30,
    font=("Arial", 20, "bold"), fg_color=None, hover_color=None, text_color="white",
    command=deslogar
    ).pack(pady=10) 

def gerenciar_atividades(janela_atual=None):
    if janela_atual:
        janela_atual.destroy()

    atividade_api = AtividadeGUI()

    janela_menu = tk.Toplevel()
    janela_menu.title("Gerenciar Atividades")
    janela_menu.geometry("1360x768")
    janela_menu.configure(bg=COR_FUNDO)

    tk.Label(janela_menu, text="Gerenciar Atividades", font=("Arial", 28, "bold"), bg=COR_FUNDO, fg="white").pack(pady=20)

    ctk.CTkButton(janela_menu, text="1 - Criar Atividade", width=400, height=60, corner_radius=30,
                  font=("Arial", 20, "bold"), command=lambda: atividade_api.criar_atividade(janela_menu)).pack(pady=10)

    ctk.CTkButton(janela_menu, text="2 - Listar Atividades", width=400, height=60, corner_radius=30,
                  font=("Arial", 20, "bold"), command=lambda: atividade_api.listar_atividades()).pack(pady=10)

    ctk.CTkButton(janela_menu, text="3 - Voltar", width=400, height=60, corner_radius=30,
                  font=("Arial", 20, "bold"), command=janela_menu.destroy).pack(pady=10)
    
def mostrar_dados_professor(janela_atual=None):
    global USUARIO_LOGADO
    if not USUARIO_LOGADO:
        messagebox.showerror("Erro", "Nenhum professor logado.")
        return

    try:
        r = requests.get(f"{API_URL}/professores")
        professores = r.json() if r.status_code == 200 else []
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "Não foi possível conectar à API.")
        return

    prof = next((p for p in professores if p["email"] == USUARIO_LOGADO["email"]), None)
    if not prof:
        messagebox.showerror("Erro", "Professor não encontrado na API.")
        return

    info = f"Nome: {prof.get('nome','')}\nEmail: {prof.get('email','')}"
    messagebox.showinfo("Perfil do Professor", info)

def editar_perfil_professor(janela_atual=None):
    global USUARIO_LOGADO
    if not USUARIO_LOGADO:
        messagebox.showerror("Erro", "Nenhum professor logado.")
        return

    editar_janela = tk.Toplevel()
    editar_janela.title("Editar Perfil")
    editar_janela.geometry("400x300")
    editar_janela.configure(bg=COR_FUNDO)

    ctk.CTkLabel(editar_janela, text="Editar Perfil", font=("Arial", 20, "bold")).pack(pady=10)

    nome_entry = ctk.CTkEntry(editar_janela, placeholder_text="Novo nome", width=300)
    nome_entry.insert(0, USUARIO_LOGADO["nome"])
    nome_entry.pack(pady=5)

    email_entry = ctk.CTkEntry(editar_janela, placeholder_text="Novo email", width=300)
    email_entry.insert(0, USUARIO_LOGADO["email"])
    email_entry.pack(pady=5)

    senha_entry = ctk.CTkEntry(editar_janela, placeholder_text="Nova senha", show="*", width=300)
    senha_entry.insert(0, USUARIO_LOGADO["senha"])
    senha_entry.pack(pady=5)

    def salvar_edicao():
        payload = {
            "nome": nome_entry.get().strip(),
            "email": email_entry.get().strip(),
            "senha": senha_entry.get().strip()
        }

        try:
            r = requests.put(f"{API_URL}/professores/{USUARIO_LOGADO['email']}", json=payload)
            if r.status_code == 200:
                messagebox.showinfo("Sucesso", "Perfil atualizado com sucesso!")
                USUARIO_LOGADO.update(payload)
                editar_janela.destroy()
            else:
                messagebox.showerror("Erro", r.json().get("detail","Erro ao atualizar perfil."))
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Erro", "Não foi possível conectar à API.")

    ctk.CTkButton(editar_janela, text="Salvar Alterações", width=200, height=40, command=salvar_edicao).pack(pady=15)

def perfil_professor_gui(janela_atual=None):
    if janela_atual:
        janela_atual.destroy()

    janela_perfil = tk.Toplevel()
    janela_perfil.title("Perfil do Professor")
    janela_perfil.geometry("1360x768")
    janela_perfil.configure(bg=COR_FUNDO)

    tk.Label(
        janela_perfil, text="Perfil do Professor", font=("Arial", 28, "bold"),
        bg=COR_FUNDO, fg="white"
    ).pack(pady=30)

    ctk.CTkButton(
        janela_perfil, text="1 - Ver Perfil", width=400, height=60, corner_radius=30,
        font=("Arial", 20, "bold"), command=lambda: mostrar_dados_professor(janela_perfil)
    ).pack(pady=10)

    ctk.CTkButton(
        janela_perfil, text="2 - Atualizar Dados", width=400, height=60, corner_radius=30,
        font=("Arial", 20, "bold"), command=lambda: editar_perfil_professor(janela_perfil)
    ).pack(pady=10)

    ctk.CTkButton(
        janela_perfil, text="3 - Deletar Perfil", width=400, height=60, corner_radius=30,
        font=("Arial", 20, "bold"), command=lambda: excluir_proprio_perfil_professor(janela_perfil)
    ).pack(pady=10)

    ctk.CTkButton(
        janela_perfil, text="4 - Voltar", width=400, height=60, corner_radius=30,
        font=("Arial", 20, "bold"), command=janela_perfil.destroy
    ).pack(pady=10)

def gerenciar_alunos_gui(janela_anterior=None):
    if janela_anterior:
        janela_anterior.withdraw()

    aluno_obj = AlunosGUI()

    janela_menu = tk.Toplevel()
    janela_menu.title("Gerenciar Alunos")
    janela_menu.geometry("800x600")
    janela_menu.configure(bg="#1a1a1a")

    tk.Label(janela_menu, text="Gerenciar Alunos", font=("Arial", 28, "bold"), fg="white", bg="#1a1a1a").pack(pady=30)

    ctk.CTkButton(janela_menu, text="1 - Criar Aluno", width=400, height=60, corner_radius=30, font=("Arial", 20, "bold"),
                  command=lambda: aluno_obj.criar_aluno(janela_menu)).pack(pady=10)
    ctk.CTkButton(janela_menu, text="2 - Listar Alunos", width=400, height=60, corner_radius=30, font=("Arial", 20, "bold"),
                  command=aluno_obj.listar_alunos).pack(pady=10)
    ctk.CTkButton(janela_menu, text="5 - Voltar", width=400, height=60, corner_radius=30, font=("Arial", 20, "bold"),
                  command=janela_menu.destroy).pack(pady=10)

    janela_menu.mainloop()

def mostrar_dados_professor(janela_anterior=None):
    global USUARIO_LOGADO

    if not USUARIO_LOGADO:
        messagebox.showwarning("Aviso", "Nenhum professor logado.")
        return

    if janela_anterior:
        janela_anterior.withdraw()

    try:
        r = requests.get(f"{API_URL}/professores/{USUARIO_LOGADO['email']}")
        if r.status_code == 200:
            prof = r.json()
        else:
            messagebox.showerror("Erro", r.json().get("detail", "Não foi possível carregar os dados."))
            return
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "Não foi possível conectar à API.")
        return

    janela_dados = tk.Toplevel()
    janela_dados.title("Meus Dados")
    janela_dados.geometry("600x400")
    janela_dados.configure(bg=COR_FUNDO)

    tk.Label(janela_dados, text="Meus Dados", font=("Arial", 28, "bold"),
             bg=COR_FUNDO, fg="white").pack(pady=20)

    tk.Label(janela_dados, text=f"Nome: {prof['nome']}", font=("Arial", 18),
             bg=COR_FUNDO, fg="white").pack(pady=10)
    tk.Label(janela_dados, text=f"E-mail: {prof['email']}", font=("Arial", 18),
             bg=COR_FUNDO, fg="white").pack(pady=10)
    tk.Label(janela_dados, text=f"Senha: {'*' * len(prof['senha'])}", font=("Arial", 18),
             bg=COR_FUNDO, fg="white").pack(pady=10)

    ctk.CTkButton(
        janela_dados, text="Voltar", width=200, height=50, corner_radius=20,
        font=("Arial", 18, "bold"),
        command=lambda: (janela_dados.destroy(), janela_anterior and janela_anterior.deiconify())
    ).pack(pady=30)

def excluir_proprio_perfil_professor(janela_atual=None):
    global USUARIO_LOGADO
    if not USUARIO_LOGADO:
        messagebox.showerror("Erro", "Nenhum professor logado.")
        return

    resposta = messagebox.askyesno("Confirmar", "Deseja realmente excluir seu perfil?")
    if not resposta:
        return

    try:
        r = requests.delete(f"{API_URL}/professores/{USUARIO_LOGADO['email']}")
        if r.status_code == 200:
            messagebox.showinfo("Conta excluída", "Seu perfil foi removido com sucesso!")
            USUARIO_LOGADO = None
            if janela_atual:
                janela_atual.destroy()
        else:
            messagebox.showerror("Erro", r.json().get("detail","Erro ao excluir perfil."))
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "Não foi possível conectar à API.")

def excluir_turma(janela_anterior=None):
    if janela_anterior:
        janela_anterior.withdraw()

    try:
        r = requests.get(f"{API_URL}/turmas")
        if r.status_code == 200:
            turmas = r.json()
        else:
            messagebox.showerror("Erro", "Não foi possível carregar as turmas.")
            return
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "Não foi possível conectar à API.")
        return

    if not turmas:
        messagebox.showinfo("Info", "Nenhuma turma cadastrada para excluir.")
        if janela_anterior:
            janela_anterior.deiconify()
        return

    janela_excluir = tk.Toplevel()
    janela_excluir.title("Excluir Turma")
    janela_excluir.geometry("600x400")
    janela_excluir.configure(bg=COR_FUNDO)

    tk.Label(janela_excluir, text="Excluir Turma", font=("Arial", 28, "bold"),
             bg=COR_FUNDO, fg="white").pack(pady=20)

    nomes_turmas = [t["nome"] for t in turmas]
    var_turma = tk.StringVar(value=nomes_turmas[0])
    tk.Label(janela_excluir, text="Selecione a turma para excluir:", font=("Arial", 20),
             bg=COR_FUNDO, fg="white").pack(pady=10)
    dropdown_turmas = ctk.CTkOptionMenu(janela_excluir, values=nomes_turmas, variable=var_turma, width=400)
    dropdown_turmas.pack(pady=10)

    def confirmar_exclusao():
        escolha = var_turma.get()
        if not escolha:
            messagebox.showerror("Erro", "Selecione uma turma para excluir.")
            return

        if messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir a turma '{escolha}'?"):
            try:
                r = requests.delete(f"{API_URL}/turmas/{escolha}")
                if r.status_code == 200:
                    messagebox.showinfo("Sucesso", f"Turma '{escolha}' excluída com sucesso!")
                    janela_excluir.destroy()
                    if janela_anterior:
                        janela_anterior.deiconify()
                else:
                    erro = r.json().get("detail", "Erro ao excluir a turma.")
                    messagebox.showerror("Erro", erro)
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Erro", "Não foi possível conectar à API.")

    ctk.CTkButton(janela_excluir, text="Excluir", width=250, height=50, corner_radius=20,
                  font=("Arial", 18, "bold"), command=confirmar_exclusao).pack(pady=15)
    ctk.CTkButton(janela_excluir, text="Cancelar", width=250, height=50, corner_radius=20,
                  font=("Arial", 18, "bold"),
                  command=lambda: (janela_excluir.destroy(), janela_anterior and janela_anterior.deiconify())).pack()

def ver_turmas(janela_anterior=None):
    if janela_anterior:
        janela_anterior.withdraw() 

    janela_ver = tk.Toplevel()
    janela_ver.title("Turmas Cadastradas")
    janela_ver.geometry("800x600")
    janela_ver.configure(bg=COR_FUNDO)

    tk.Label(janela_ver, text="Turmas Cadastradas", font=("Arial", 28, "bold"),
             bg=COR_FUNDO, fg="white").pack(pady=20)

    frame_lista = tk.Frame(janela_ver, bg=COR_FUNDO)
    frame_lista.pack(fill="both", expand=True, padx=20, pady=10)

    try:
        r = requests.get(f"{API_URL}/turmas")
        if r.status_code == 200:
            turmas = r.json()
        else:
            messagebox.showerror("Erro", "Não foi possível carregar as turmas.")
            turmas = []
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "Não foi possível conectar à API.")
        turmas = []

    if not turmas:
        tk.Label(frame_lista, text="Nenhuma turma cadastrada.", font=("Arial", 20),
                 bg=COR_FUNDO, fg="white").pack(pady=10)
    else:
        for i, turma in enumerate(turmas, start=1):
            texto_turma = f"{i}. {turma['nome']} - Professor: {turma.get('professor', 'Desconhecido')}"
            tk.Label(frame_lista, text=texto_turma, font=("Arial", 18),
                     bg=COR_FUNDO, fg="white").pack(anchor="w", pady=(5,0))
            alunos = turma.get("alunos", [])
            if alunos:
                for aluno in alunos:
                    tk.Label(frame_lista, text=f"   - {aluno}", font=("Arial", 16),
                             bg=COR_FUNDO, fg="white").pack(anchor="w")
            else:
                tk.Label(frame_lista, text="   Nenhum aluno nesta turma.", font=("Arial", 16),
                         bg=COR_FUNDO, fg="white").pack(anchor="w")

    def voltar():
        janela_ver.destroy()
        if janela_anterior:
            janela_anterior.deiconify()

    ctk.CTkButton(janela_ver, text="Voltar", width=200, height=50, corner_radius=20,
                  font=("Arial", 18, "bold"), command=voltar).pack(pady=20)

def alterar_turmas(janela_anterior=None):
    if janela_anterior:
        janela_anterior.withdraw() 

    # Buscar turmas via API
    try:
        r = requests.get(f"{API_URL}/turmas")
        if r.status_code == 200:
            turmas = r.json()
        else:
            messagebox.showerror("Erro", "Não foi possível carregar as turmas.")
            turmas = []
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "Não foi possível conectar à API.")
        turmas = []

    if not turmas:
        messagebox.showinfo("Info", "Nenhuma turma cadastrada para alterar.")
        if janela_anterior:
            janela_anterior.deiconify()
        return

    janela_alterar = tk.Toplevel()
    janela_alterar.title("Alterar Turma")
    janela_alterar.geometry("600x500")
    janela_alterar.configure(bg=COR_FUNDO)

    tk.Label(janela_alterar, text="Alterar Turma", font=("Arial", 28, "bold"),
             bg=COR_FUNDO, fg="white").pack(pady=20)

    tk.Label(janela_alterar, text="Escolha a turma:", font=("Arial", 20), bg=COR_FUNDO, fg="white").pack(pady=(10,0))
    nomes_turmas = [t["nome"] for t in turmas]
    var_turma = tk.StringVar(value=nomes_turmas[0])
    dropdown_turmas = ctk.CTkOptionMenu(janela_alterar, values=nomes_turmas, variable=var_turma, width=400)
    dropdown_turmas.pack(pady=10)

    tk.Label(janela_alterar, text="Novo nome da turma:", font=("Arial", 20), bg=COR_FUNDO, fg="white").pack(pady=(10,0))
    entry_novo_nome = ctk.CTkEntry(janela_alterar, width=400, height=40, font=("Arial", 16))
    entry_novo_nome.pack(pady=5)

    tk.Label(janela_alterar, text="Novo professor:", font=("Arial", 20), bg=COR_FUNDO, fg="white").pack(pady=(10,0))
    entry_novo_prof = ctk.CTkEntry(janela_alterar, width=400, height=40, font=("Arial", 16))
    entry_novo_prof.pack(pady=5)

    def salvar_alteracao():
        escolha = var_turma.get()
        turma = next((t for t in turmas if t["nome"] == escolha), None)
        if not turma:
            messagebox.showerror("Erro", f"Turma '{escolha}' não encontrada!")
            return

        novo_nome = entry_novo_nome.get().strip() or turma["nome"]
        novo_professor = entry_novo_prof.get().strip() or turma.get("professor", "")

        payload = {
            "turma_antiga": escolha,
            "novo_nome": novo_nome,
            "novo_professor": novo_professor
        }

        try:
            r = requests.put(f"{API_URL}/alterar_turma", json=payload)
            if r.status_code == 200:
                messagebox.showinfo("Sucesso", f"Turma '{escolha}' alterada com sucesso!")
                janela_alterar.destroy()
                if janela_anterior:
                    janela_anterior.deiconify()
            else:
                erro = r.json().get("detail", "Erro ao alterar a turma.")
                messagebox.showerror("Erro", erro)
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Erro", "Não foi possível conectar à API.")

    ctk.CTkButton(janela_alterar, text="Salvar Alteração", width=250, height=50, corner_radius=20,
                  font=("Arial", 18, "bold"), command=salvar_alteracao).pack(pady=15)
    ctk.CTkButton(janela_alterar, text="Cancelar", width=250, height=50, corner_radius=20,
                  font=("Arial", 18, "bold"),
                  command=lambda: (janela_alterar.destroy(), janela_anterior and janela_anterior.deiconify())).pack()

def cadastrar_turmas(janela_anterior=None):
    if janela_anterior:
        janela_anterior.withdraw() 

    janela_cadastro = tk.Toplevel()
    janela_cadastro.title("Cadastrar Turma")
    janela_cadastro.geometry("600x400")
    janela_cadastro.configure(bg=COR_FUNDO)

    tk.Label(janela_cadastro, text="Cadastrar Nova Turma", font=("Arial", 28, "bold"),
             bg=COR_FUNDO, fg="white").pack(pady=20)

    tk.Label(janela_cadastro, text="Nome da Turma:", font=("Arial", 20), bg=COR_FUNDO, fg="white").pack(pady=(10,0))
    entry_nome = ctk.CTkEntry(janela_cadastro, width=400, height=40, font=("Arial", 16))
    entry_nome.pack(pady=5)

    tk.Label(janela_cadastro, text="Professor:", font=("Arial", 20), bg=COR_FUNDO, fg="white").pack(pady=(10,0))
    entry_professor = ctk.CTkEntry(janela_cadastro, width=400, height=40, font=("Arial", 16))
    entry_professor.pack(pady=5)

    def salvar():
        nome = entry_nome.get().strip()
        professor = entry_professor.get().strip()

        if not nome or not professor:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
            return

        payload = {"nome": nome, "professor": professor}

        try:
            r = requests.post(f"{API_URL}/cadastrar_turma", json=payload)
            if r.status_code == 200:
                messagebox.showinfo("Sucesso", f"Turma '{nome}' cadastrada com sucesso!")
                janela_cadastro.destroy()
                if janela_anterior:
                    janela_anterior.deiconify()
            else:
                erro = r.json().get("detail", "Erro ao cadastrar a turma.")
                messagebox.showerror("Erro", erro)
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Erro", "Não foi possível conectar à API.")

    ctk.CTkButton(janela_cadastro, text="Salvar", width=200, height=50, corner_radius=20,
                  font=("Arial", 18, "bold"), command=salvar).pack(pady=15)
    ctk.CTkButton(janela_cadastro, text="Cancelar", width=200, height=50, corner_radius=20,
                  font=("Arial", 18, "bold"), command=lambda: (janela_cadastro.destroy(), janela_anterior and janela_anterior.deiconify())).pack()

def professor():
    janela.withdraw()
    janela_prof = tk.Toplevel()
    janela_prof.title("Área do Professor")
    janela_prof.geometry("1360x768")
    janela_prof.configure(bg=COR_FUNDO)


    tk.Label(janela_prof, text="Bem-vindo, Professor!", font=("Arial", 28, "bold"),
             bg=COR_FUNDO, fg="white").pack(pady=40)

    ctk.CTkButton(janela_prof, text="Logar", width=400, height=70, corner_radius=35,
                  fg_color=None, hover_color=None, text_color="white", font=("Arial", 24, "bold"),
                  command=lambda: logar_professor(janela_prof)).pack(pady=10)

    ctk.CTkButton(janela_prof, text="Cadastrar", width=400, height=70, corner_radius=35,
                  fg_color=None, hover_color=None, text_color="white", font=("Arial", 24, "bold"),
                  command=cadastrar_professor).pack(pady=10)

    ctk.CTkButton(janela_prof, text="Voltar", width=400, height=70, corner_radius=35,
                  fg_color=None, hover_color=None, text_color="white", font=("Arial", 24, "bold"),
                  command=lambda: voltar_para_menu(janela_prof)).pack(pady=10)

def voltar_para_menu(janela_prof):
    janela_prof.destroy()
    janela.deiconify()

class AtividadeGUI:
    def __init__(self):
        self.turma = ""
        self.pergunta = ""
        self.alternativas = {"A": "", "B": "", "C": "", "D": ""}
        self.correta = ""

    def criar_atividade(self, janela_atual=None):
        if janela_atual:
            janela_atual.destroy()

        self.janela = tk.Toplevel()
        self.janela.title("Criar Atividade")
        self.janela.geometry("800x1000")
        self.janela.configure(bg="#1a1a1a")

        tk.Label(self.janela, text="Criar Atividade", font=("Arial", 28, "bold"),
                 bg="#1a1a1a", fg="white").pack(pady=20)

        tk.Label(self.janela, text="Turma:", font=("Arial", 20), bg="#1a1a1a", fg="white").pack(pady=(10,0))
        self.entry_turma = ctk.CTkEntry(self.janela, width=400, height=50, font=("Arial", 18))
        self.entry_turma.pack(pady=5)

        tk.Label(self.janela, text="Pergunta:", font=("Arial", 20), bg="#1a1a1a", fg="white").pack(pady=(10,0))
        self.entry_pergunta = ctk.CTkEntry(self.janela, width=600, height=50, font=("Arial", 18))
        self.entry_pergunta.pack(pady=5)

        self.entry_alt = {}
        for letra in ["A", "B", "C", "D"]:
            tk.Label(self.janela, text=f"{letra})", font=("Arial", 20), bg="#1a1a1a", fg="white").pack(pady=(5,0))
            self.entry_alt[letra] = ctk.CTkEntry(self.janela, width=500, height=50, font=("Arial", 18))
            self.entry_alt[letra].pack(pady=5)

        tk.Label(self.janela, text="Alternativa correta (A/B/C/D):", font=("Arial", 20), bg="#1a1a1a", fg="white").pack(pady=(10,0))
        self.entry_correta = ctk.CTkEntry(self.janela, width=100, height=50, font=("Arial", 18))
        self.entry_correta.pack(pady=5)

        ctk.CTkButton(self.janela, text="Salvar Atividade", width=300, height=60, corner_radius=30,
                      font=("Arial", 20, "bold"), command=self.salvar_atividade).pack(pady=20)

        ctk.CTkButton(self.janela, text="Cancelar", width=300, height=60, corner_radius=30,
                      font=("Arial", 20, "bold"), command=self.janela.destroy).pack()

    def salvar_atividade(self):
        self.turma = self.entry_turma.get().strip()
        self.pergunta = self.entry_pergunta.get().strip()
        for letra in ["A", "B", "C", "D"]:
            self.alternativas[letra] = self.entry_alt[letra].get().strip()
        self.correta = self.entry_correta.get().strip().upper()

        if not self.turma or not self.pergunta or any(not v for v in self.alternativas.values()) or self.correta not in ["A", "B", "C", "D"]:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente!")
            return

        payload = {
            "turma": self.turma,
            "pergunta": self.pergunta,
            "alternativas": self.alternativas,
            "correta": self.correta
        }

        try:
            r = requests.post(f"{API_URL}/atividades", json=payload)
            if r.status_code == 200:
                messagebox.showinfo("Sucesso", "Atividade criada com sucesso via API!")
                self.janela.destroy()
            else:
                erro = r.json().get("detail", "Erro ao criar atividade.")
                messagebox.showerror("Erro", erro)
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Erro", "Não foi possível conectar à API.")

    def listar_atividades(self):
        try:
            r = requests.get(f"{API_URL}/atividades")
            if r.status_code != 200:
                messagebox.showerror("Erro", "Não foi possível obter atividades da API.")
                return
            atividades = r.json()
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Erro", "Não foi possível conectar à API.")
            return

        janela = tk.Toplevel()
        janela.title("Lista de Atividades")
        janela.geometry("800x600")
        janela.configure(bg="#1a1a1a")

        ctk.CTkLabel(janela, text="Lista de Atividades", font=("Arial", 24, "bold")).pack(pady=20)

        if not atividades:
            ctk.CTkLabel(janela, text="Nenhuma atividade cadastrada.", font=("Arial", 18)).pack(pady=20)
            return

        frame_scroll = ctk.CTkScrollableFrame(janela, width=760, height=500)
        frame_scroll.pack(pady=10, padx=20)

        for i, atv in enumerate(atividades, start=1):
            turma = atv.get("turma", "N/A")
            pergunta = atv.get("pergunta", "N/A")
            correta = atv.get("correta", "N/A")
            texto = f"{i}. Turma: {turma} | Pergunta: {pergunta} | Correta: {correta}"
            ctk.CTkLabel(frame_scroll, text=texto, font=("Arial", 16), anchor="w").pack(fill="x", pady=5)

class TurmaGUI:
    def criar_turma(self, janela_atual=None):
        if janela_atual:
            janela_atual.destroy()

        self.janela = tk.Toplevel()
        self.janela.title("Criar Turma")
        self.janela.geometry("700x500")
        self.janela.configure(bg="#1a1a1a")

        tk.Label(self.janela, text="Criar Turma", font=("Arial", 28, "bold"),
                 bg="#1a1a1a", fg="white").pack(pady=20)

        tk.Label(self.janela, text="Nome da turma:", font=("Arial", 20),
                 bg="#1a1a1a", fg="white").pack(pady=(10, 0))
        self.entry_nome = ctk.CTkEntry(self.janela, width=400, height=50, font=("Arial", 18))
        self.entry_nome.pack(pady=5)

        tk.Label(self.janela, text="Professor:", font=("Arial", 20),
                 bg="#1a1a1a", fg="white").pack(pady=(10, 0))
        self.entry_professor = ctk.CTkEntry(self.janela, width=400, height=50, font=("Arial", 18))
        self.entry_professor.pack(pady=5)

        ctk.CTkButton(self.janela, text="Salvar", width=300, height=60, corner_radius=30,
                      font=("Arial", 20, "bold"), command=self.salvar_turma).pack(pady=20)
        ctk.CTkButton(self.janela, text="Cancelar", width=300, height=60, corner_radius=30,
                      font=("Arial", 20, "bold"), command=self.janela.destroy).pack()

    def salvar_turma(self):
        nome = self.entry_nome.get().strip()
        professor = self.entry_professor.get().strip()

        if not nome or not professor:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
            return

        payload = {
            "nome": nome,
            "professor": professor
        }
        try:
            r = requests.post(f"{API_URL}/turmas", json=payload)
            if r.status_code == 200:
                messagebox.showinfo("Sucesso", f"Turma '{nome}' cadastrada com sucesso via API!")
                self.janela.destroy()
            else:
                erro = r.json().get("detail", "Erro ao criar turma.")
                messagebox.showerror("Erro", erro)
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Erro", "Não foi possível conectar à API.")

    def listar_turmas(self):
        try:
            r = requests.get(f"{API_URL}/turmas")
            if r.status_code != 200:
                messagebox.showerror("Erro", "Não foi possível obter turmas da API.")
                return
            turmas = r.json()
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Erro", "Não foi possível conectar à API.")
            return

        janela = tk.Toplevel()
        janela.title("Lista de Turmas")
        janela.geometry("800x600")
        janela.configure(bg="#1a1a1a")

        ctk.CTkLabel(janela, text="Lista de Turmas", font=("Arial", 24, "bold")).pack(pady=20)

        if not turmas:
            ctk.CTkLabel(janela, text="Nenhuma turma cadastrada.", font=("Arial", 18)).pack(pady=20)
            return

        frame_scroll = ctk.CTkScrollableFrame(janela, width=760, height=500)
        frame_scroll.pack(pady=10, padx=20)

        for i, t in enumerate(turmas, start=1):
            texto = f"{i}. {t['nome']} - Professor: {t['professor']}"
            ctk.CTkLabel(frame_scroll, text=texto, font=("Arial", 16), anchor="w").pack(fill="x", pady=5)

class AlunosGUI:
    def criar_aluno(self, janela_anterior=None):
        if janela_anterior:
            janela_anterior.withdraw()

        janela = tk.Toplevel()
        janela.title("Criar Aluno")
        janela.geometry("400x400")
        janela.configure(bg="#1a1a1a")

        tk.Label(janela, text="Nome:", bg="#1a1a1a", fg="white").pack(pady=5)
        entry_nome = tk.Entry(janela, width=30)
        entry_nome.pack(pady=5)

        tk.Label(janela, text="NP1:", bg="#1a1a1a", fg="white").pack(pady=5)
        entry_np1 = tk.Entry(janela, width=30)
        entry_np1.pack(pady=5)

        tk.Label(janela, text="NP2:", bg="#1a1a1a", fg="white").pack(pady=5)
        entry_np2 = tk.Entry(janela, width=30)
        entry_np2.pack(pady=5)

        tk.Label(janela, text="Turma:", bg="#1a1a1a", fg="white").pack(pady=5)
        entry_turma = tk.Entry(janela, width=30)
        entry_turma.pack(pady=5)

        def salvar():
            nome = entry_nome.get().strip()
            try:
                np1 = float(entry_np1.get())
                np2 = float(entry_np2.get())
            except ValueError:
                messagebox.showerror("Erro", "NP1 e NP2 devem ser números!")
                return
            turma = entry_turma.get().strip()

            payload = {"nome": nome, "np1": np1, "np2": np2, "turma": turma}

            try:
                r = requests.post(f"{API_URL}/cadastro/aluno", json=payload)
                if r.status_code == 200:
                    messagebox.showinfo("Sucesso", f"Aluno '{nome}' adicionado à turma '{turma}'!")
                    janela.destroy()
                else:
                    messagebox.showerror("Erro", r.json().get("detail", "Erro ao criar aluno"))
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Erro", "Não foi possível conectar à API.")

        ctk.CTkButton(janela, text="Salvar", width=200, height=40, corner_radius=20, command=salvar).pack(pady=20)

    def listar_alunos(self):
        try:
            r = requests.get(f"{API_URL}/alunos")
            alunos = r.json() if r.status_code == 200 else []
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Erro", "Não foi possível conectar à API.")
            return

        janela = tk.Toplevel()
        janela.title("Lista de Alunos")
        janela.geometry("800x600")
        janela.configure(bg="#1a1a1a")

        ctk.CTkLabel(janela, text="Lista de Alunos", font=("Arial", 24, "bold")).pack(pady=20)

        if not alunos:
            ctk.CTkLabel(janela, text="Nenhum aluno cadastrado.", font=("Arial", 18)).pack(pady=20)
            return

        frame_scroll = ctk.CTkScrollableFrame(janela, width=760, height=500)
        frame_scroll.pack(pady=10, padx=20)

        for aluno in alunos:
            turmas = aluno.get("turmas", [])
            if not isinstance(turmas, list):
                turmas = [str(turmas)]
            info = f"{aluno.get('nome','N/A')} - NP1: {aluno.get('np1','N/A')} | NP2: {aluno.get('np2','N/A')} | Turmas: {', '.join(turmas)}"
            ctk.CTkLabel(frame_scroll, text=info, font=("Arial", 16), anchor="w").pack(fill="x", pady=5)

    def atualizar_aluno(self):
        try:
            r = requests.get(f"{API_URL}/alunos")
            alunos = r.json() if r.status_code == 200 else []
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Erro", "Não foi possível conectar à API.")
            return

        if not alunos:
            messagebox.showinfo("Info", "Nenhum aluno cadastrado.")
            return

        janela = tk.Toplevel()
        janela.title("Atualizar Aluno")
        janela.geometry("400x450")
        janela.configure(bg="#1a1a1a")

        nomes = [a['nome'] for a in alunos]
        tk.Label(janela, text="Escolha o aluno:", bg="#1a1a1a", fg="white").pack(pady=5)
        var = tk.StringVar(janela)
        var.set(nomes[0])
        tk.OptionMenu(janela, var, *nomes).pack(pady=5)

        tk.Label(janela, text="Novo nome:", bg="#1a1a1a", fg="white").pack(pady=5)
        entry_nome = tk.Entry(janela, width=30)
        entry_nome.pack(pady=5)

        tk.Label(janela, text="Nova NP1:", bg="#1a1a1a", fg="white").pack(pady=5)
        entry_np1 = tk.Entry(janela, width=30)
        entry_np1.pack(pady=5)

        tk.Label(janela, text="Nova NP2:", bg="#1a1a1a", fg="white").pack(pady=5)
        entry_np2 = tk.Entry(janela, width=30)
        entry_np2.pack(pady=5)

        tk.Label(janela, text="Nova turma:", bg="#1a1a1a", fg="white").pack(pady=5)
        entry_turma = tk.Entry(janela, width=30)
        entry_turma.pack(pady=5)

        def salvar():
            aluno_selecionado = var.get()
            payload = {
                "nome": entry_nome.get().strip(),
                "np1": entry_np1.get().strip(),
                "np2": entry_np2.get().strip(),
                "turma": entry_turma.get().strip()
            }
            try:
                r = requests.put(f"{API_URL}/aluno/{aluno_selecionado}", json=payload)
                if r.status_code == 200:
                    messagebox.showinfo("Sucesso", "Aluno atualizado!")
                    janela.destroy()
                else:
                    messagebox.showerror("Erro", r.json().get("detail", "Erro ao atualizar aluno"))
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Erro", "Não foi possível conectar à API.")

        ctk.CTkButton(janela, text="Salvar", width=200, height=40, corner_radius=20, command=salvar).pack(pady=20)

    def excluir_aluno(self):
        try:
            r = requests.get(f"{API_URL}/alunos")
            alunos = r.json() if r.status_code == 200 else []
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Erro", "Não foi possível conectar à API.")
            return

        if not alunos:
            messagebox.showinfo("Info", "Nenhum aluno cadastrado.")
            return

        janela = tk.Toplevel()
        janela.title("Excluir Aluno")
        janela.geometry("400x300")
        janela.configure(bg="#1a1a1a")

        nomes = [a['nome'] for a in alunos]
        tk.Label(janela, text="Escolha o aluno:", bg="#1a1a1a", fg="white").pack(pady=5)
        var = tk.StringVar(janela)
        var.set(nomes[0])
        tk.OptionMenu(janela, var, *nomes).pack(pady=5)

        def deletar():
            aluno_selecionado = var.get()
            try:
                r = requests.delete(f"{API_URL}/aluno/{aluno_selecionado}")
                if r.status_code == 200:
                    messagebox.showinfo("Sucesso", "Aluno excluído!")
                    janela.destroy()
                else:
                    messagebox.showerror("Erro", r.json().get("detail", "Erro ao excluir aluno"))
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Erro", "Não foi possível conectar à API.")

        ctk.CTkButton(janela, text="Excluir", width=200, height=40, corner_radius=20, command=deletar).pack(pady=20)


janela = tk.Tk()
janela.title("BX ensino & aprendizagem!")
janela.geometry("1360x768")
janela.configure(bg=COR_FUNDO)

caminho_logo = os.path.join("imagens", "logo.png")
if os.path.exists(caminho_logo):
    img_logo = aplicar_fundo_azul(Image.open(caminho_logo).resize((450, 450)))
    logo = ImageTk.PhotoImage(img_logo)
    label_logo = tk.Label(janela, image=logo, bg=COR_FUNDO)
    label_logo.place(x=460, y=-10)
    label_logo.image = logo

ctk.CTkButton(janela, text="Logar como Aluno", width=400, height=70, corner_radius=35,
              fg_color=None, hover_color=None, text_color="white", font=("Arial", 24, "bold"),
              command=aluno).place(x=500, y=350)

ctk.CTkButton(janela, text="Logar como Professor", width=400, height=70, corner_radius=35,
              fg_color=None, hover_color=None, text_color="white", font=("Arial", 24, "bold"),
              command=professor).place(x=500, y=450)

ctk.CTkButton(janela, text="Fale Conosco", width=400, height=70, corner_radius=35,
              fg_color=None, hover_color=None, text_color="white", font=("Arial", 24, "bold"),
              command=fale_conosco).place(x=500, y=550)

ctk.CTkButton(janela, text="Sair", width=400, height=70, corner_radius=35,
              fg_color=None, hover_color=None, text_color="white", font=("Arial", 24, "bold"),
              command=janela.destroy).place(x=500, y=650)

if __name__ == "__main__":
    janela.mainloop()
