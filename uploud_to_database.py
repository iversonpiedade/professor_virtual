# Importa a biblioteca 
import streamlit_authenticator as stauth
# Importa a base de dados
import database as db

# Define uma lista de usuários
usuarios = ["azua"]
# Define uma lista de nomes
nomes = ["Augusto Zua"]
# Define uma lista de senhas
senhas = ["augusto123"]
# Cria uma lista de senhas criptografadas usando o módulo Streamlit-Authenticator
senhas_criptografadas = stauth.Hasher(senhas).generate()

# Itera sobre as três listas ao mesmo tempo
for (usuarios, nomes, senhas_criptografadas) in zip(usuarios, nomes, senhas_criptografadas):
    db.inserir_usuario(usuarios, nomes, senhas_criptografadas)
  
    