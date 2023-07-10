import streamlit_authenticator as stauth

import database as db

usuarios = ["azua", "hzidane"]
nomes = ["Augusto Zua", "Hélvio Zidane"]
senhas = ["augusto123", "helvio321"]
senhas_criptografadas = stauth.Hasher(senhas).generate()


for (usuarios, nomes, senhas_criptografadas) in zip(usuarios, nomes, senhas_criptografadas):
    db.inserir_usuario(usuarios, nomes, senhas_criptografadas)
    