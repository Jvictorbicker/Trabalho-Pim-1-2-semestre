from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import os
import uuid
from typing import Optional
import time
import sys

CACHE = {}
CACHE_TEMPO = 60

def conectar():
    return sqlite3.connect("dados.db")

def criar_tabelas():
    con = conectar()
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS professores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS turmas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL,
        professor TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS atividades (
        id TEXT PRIMARY KEY,
        turma TEXT NOT NULL,
        pergunta TEXT NOT NULL,
        alternativa_a TEXT,
        alternativa_b TEXT,
        alternativa_c TEXT,
        alternativa_d TEXT,
        correta TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS respostas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_email TEXT,
        atividade_id TEXT,
        resposta TEXT,
        correta TEXT
    )
    """)
    con.commit()
    con.close()

criar_tabelas()

#uvicorn servidor_api:app --reload

def resource_path(rel):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, rel)
    return rel

def conectar():
    return sqlite3.connect(resource_path("dados.db"))

def get_tabela_com_cache(tabela: str, query=None):
    """
    Retorna dados de uma tabela com cache.
    - tabela: nome da tabela
    - query: string SQL customizada (opcional)
    """
    global CACHE
    agora = time.time()

    # Verifica cache
    if tabela in CACHE:
        dados_cache, timestamp = CACHE[tabela]
        if agora - timestamp < CACHE_TEMPO:
            print(f"🔹 Retornando {tabela} do cache")
            return dados_cache

    # Consulta banco
    con = conectar()
    cur = con.cursor()
    if query:
        cur.execute(query)
    else:
        cur.execute(f"SELECT * FROM {tabela}")
    colunas = [desc[0] for desc in cur.description]
    dados = [dict(zip(colunas, row)) for row in cur.fetchall()]
    con.close()

    # Atualiza cache
    CACHE[tabela] = (dados, agora)
    print(f"🔹 Buscando {tabela} do banco")
    return dados

class Login(BaseModel):
    email: str
    senha: str

class Aluno(BaseModel):
    nome: str
    email: str
    senha: str

class RespostaAtividade(BaseModel):
    usuario_email: str
    atividade_id: str
    resposta: str

class Professor(BaseModel):
    nome: str
    email: str
    senha: str

class Turma(BaseModel):
    nome: str
    professor: str

class AlterarTurma(BaseModel):
    nome_atual: Optional[str] = None 
    novo_nome: str
    professor: Optional[str] = None

class Atividade(BaseModel):
    turma: str
    pergunta: str
    alternativas: dict
    correta: str

app = FastAPI()

@app.post("/login")
def login_usuario(login_data: Login):
    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT * FROM professores WHERE email=? AND senha=?", (login_data.email, login_data.senha))
    prof = cur.fetchone()
    if prof:
        con.close()
        return {"status": "sucesso", "tipo": "professor", "usuario": {"nome": prof[1], "email": prof[2]}}

    cur.execute("SELECT * FROM alunos WHERE email=? AND senha=?", (login_data.email, login_data.senha))
    aluno = cur.fetchone()
    con.close()
    if aluno:
        return {"status": "sucesso", "tipo": "aluno", "usuario": {"nome": aluno[1], "email": aluno[2]}}

    raise HTTPException(status_code=401, detail="Credenciais inválidas.")

@app.post("/cadastro/professor")
def cadastrar_professor(prof: Professor):
    con = conectar()
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO professores (nome, email, senha) VALUES (?, ?, ?)", (prof.nome, prof.email, prof.senha))
        con.commit()
        CACHE.pop("professores", None)  # limpa cache após inserção
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    finally:
        con.close()
    return {"status": "sucesso", "mensagem": "Professor cadastrado com sucesso!"}

@app.post("/cadastro/aluno")
def cadastrar_aluno(aluno: Aluno):
    con = conectar()
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO alunos (nome, email, senha) VALUES (?, ?, ?)", (aluno.nome, aluno.email, aluno.senha))
        con.commit()
        CACHE.pop("alunos", None)  # limpa cache
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    finally:
        con.close()
    return {"status": "sucesso", "mensagem": "Aluno cadastrado com sucesso!"}

@app.get("/alunos")
def listar_alunos():
    return get_tabela_com_cache("alunos")

@app.get("/professores")
def listar_professores():
    return get_tabela_com_cache("professores")

@app.get("/turmas")
def listar_turmas():
    return get_tabela_com_cache("turmas")

@app.post("/cadastrar_turma")
def cadastrar_turma(turma: Turma):
    con = conectar()
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO turmas (nome, professor) VALUES (?, ?)", (turma.nome, turma.professor))
        con.commit()
        CACHE.pop("turmas", None)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Turma já existe.")
    finally:
        con.close()
    return {"status": "sucesso", "mensagem": f"Turma '{turma.nome}' cadastrada com sucesso!"}
    
@app.put("/alterar_turma")
def alterar_turma(dados_turma: AlterarTurma):
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM turmas WHERE nome=?", (dados_turma.nome_atual,))
    turma = cur.fetchone()
    if not turma:
        con.close()
        raise HTTPException(status_code=404, detail="Turma não encontrada.")
    cur.execute("UPDATE turmas SET nome=?, professor=? WHERE nome=?", 
                (dados_turma.novo_nome, dados_turma.professor, dados_turma.nome_atual))
    con.commit()
    con.close()
    CACHE.pop("turmas", None)  # limpa cache
    return {"status": "sucesso", "mensagem": f"Turma '{dados_turma.nome_atual}' alterada com sucesso!"}

@app.post("/atividades")
def criar_atividade(atividade: Atividade):
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT nome FROM turmas WHERE nome=?", (atividade.turma,))
    if not cur.fetchone():
        con.close()
        raise HTTPException(status_code=404, detail="Turma não encontrada.")

    nova_id = str(uuid.uuid4())
    alt = atividade.alternativas
    cur.execute("""
        INSERT INTO atividades (id, turma, pergunta, alternativa_a, alternativa_b, alternativa_c, alternativa_d, correta)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (nova_id, atividade.turma, atividade.pergunta, alt.get("A"), alt.get("B"), alt.get("C"), alt.get("D"), atividade.correta))
    con.commit()
    con.close()
    CACHE.pop("atividades", None)
    return {"status": "sucesso", "mensagem": "Atividade criada com sucesso!", "id": nova_id}

@app.get("/atividades")
def listar_atividades():
    return get_tabela_com_cache("atividades")

@app.delete("/atividades/{atividade_id}")
def excluir_atividade(atividade_id: str):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM atividades WHERE id=?", (atividade_id,))
    if cur.rowcount == 0:
        con.close()
        raise HTTPException(status_code=404, detail="Atividade não encontrada.")
    con.commit()
    con.close()
    CACHE.pop("atividades", None)
    return {"status": "sucesso", "mensagem": "Atividade removida com sucesso!"}

@app.post("/responder_atividade")
def responder_atividade(resposta: RespostaAtividade):
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM alunos WHERE email=?", (resposta.usuario_email,))
    aluno = cur.fetchone()
    if not aluno:
        con.close()
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")

    cur.execute("SELECT correta FROM atividades WHERE id=?", (resposta.atividade_id,))
    atividade = cur.fetchone()
    if not atividade:
        con.close()
        raise HTTPException(status_code=404, detail="Atividade não encontrada.")

    correta = atividade[0].upper()
    resultado = "✅ Resposta correta!" if resposta.resposta.upper() == correta else f"❌ Errado — correta: {correta}"

    # Salva resposta
    cur.execute("INSERT INTO respostas (usuario_email, atividade_id, resposta, correta) VALUES (?, ?, ?, ?)",
                (resposta.usuario_email, resposta.atividade_id, resposta.resposta.upper(), correta))
    con.commit()
    con.close()
    CACHE.pop("respostas", None)
    return {"resultado": resultado}

@app.get("/respostas")
def listar_respostas():
    return get_tabela_com_cache("respostas")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    input("Pressione ENTER para sair...")