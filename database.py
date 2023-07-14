# Importa as bibliotecas
import os
from deta import Deta  # pip install deta
from dotenv import load_dotenv  # pip install python-dotenv


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(".env")
DETA_KEY = os.getenv("DETA_KEY")

# Obtém o valor da variável de ambiente DETA_KEY, que é a chave do projeto Deta
deta = Deta(DETA_KEY)

# Cria ou conecta um banco de dados chamado “alunos” usando o método deta.Base
db = deta.Base("alunos")

# Define uma função para inserir um novo usuário no banco de dados
def inserir_usuario(usuario, nome, senha):
    # Retorna o usuário criado com sucesso, caso contrário lança um erro
    return db.put({"key": usuario, "nome": nome, "senha": senha})

# Define uma função para receber todos os usuários do banco de dados
def receber_todos_usuarios():
    # Retorna um dicionário com todos os usuários
    res = db.fetch()
    return res.items

# Define uma função para receber um usuário específico do banco de dados
def receber_usuario(usuario):
    # Se não encontrado, a função retornará None
    return db.get(usuario)

# Define uma função para atualizar um usuário existente no banco de dados
def actualizar_usuario(usuario, actualizacoes):
    # Se o item for atualizado, retorna None. Caso contrário, lança uma exceção
    return db.update(actualizacoes, usuario)

# Define uma função para apagar um usuário do banco de dados
def apagar_usuario(usuario):
    # Sempre retorna None, mesmo se a chave não existir
    return db.delete(usuario)