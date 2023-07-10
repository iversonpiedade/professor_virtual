import os

from deta import Deta  # pip install deta
from dotenv import load_dotenv  # pip install python-dotenv


# Load the environment variables
load_dotenv(".env")
DETA_KEY = os.getenv("DETA_KEY")

# Initialize with a project key
deta = Deta(DETA_KEY)

# This is how to create/connect a database
db = deta.Base("alunos")


def inserir_usuario(usuario, nome, senha):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db.put({"key": usuario, "nome": nome, "senha": senha})


def receber_todos_usuarios():
    """Returns a dict of all users"""
    res = db.fetch()
    return res.items


def receber_usuario(usuario):
    """If not found, the function will return None"""
    return db.get(usuario)


def actualizar_usuario(usuario, actualizacoes):
    """If the item is updated, returns None. Otherwise, an exception is raised"""
    return db.update(actualizacoes, usuario)


def apagar_usuario(usuario):
    """Always returns None, even if the key does not exist"""
    return db.delete(usuario)