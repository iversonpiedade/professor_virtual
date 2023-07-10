# Importando as bibliotecas 
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import openai 
import streamlit as st
from streamlit_chat import message 
import database as db 


st.set_page_config(
    page_title="Professor Virtual",
    page_icon="👨‍🏫"
)



# --- USER AUTHENTICATION ---
alunos = db.receber_todos_usuarios()

usuarios = [usuario["key"] for usuario in alunos]
names = [usuario["nome"] for usuario in alunos]
senhas_criptografadas = [usuario["senha"] for usuario in alunos]

credentials = {"usernames": {}}
for i in range(len(usuarios)):
    credentials["usernames"][usuarios[i]] = {
        "name": names[i],
        "password": senhas_criptografadas[i]
    }

authenticator = stauth.Authenticate(credentials, "professor_virtual", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Portal do aluno", "main")

if authentication_status  == True:
    authenticator.logout('Sair da Conta', 'main', key='unique_key')
    st.write(f'Olá *{name}*!')
    option = st.selectbox(
            'Em que disciplina precisa de ajuda hoje?',
            ('TIC (Tecnologias de Informação e Comunicação)', 'Matemática', "EDP (Ética e Deontologia Profissional)", "Seac (Sistema de Exploração e Arquitetura de Computadores)", "Electrotecnia","Físico-química","OGI", "Empreendedorismo", "Língua portuguesa", "Língua inglesa"))
    
    openai.api_key = st.secrets["api_secret"]
    model = "gpt-3.5-turbo"

    # Função que fará a geração de chamadas da API
    def get_initial_message():
        messages=[
            {"role": "system", "content": " És um professor especialista em " + option + " com o objectivo de esclarecer dúvidas e guiar o aluno à uma solução. OBS: Não dê a resposta logo, guie o aluno através de perguntas até que a dúvida seja esclarecida e não foge do tópico. Não responda questões muito fora do sua especialidade, Escreva de forma humanizada."},
            {"role": "assistant", "content": "Olá, serei o teu professor daqui para frente, qual é a sua dúvida em relação a " + option},
            {"role": "user", "content": "Aluno:"}
            ]
        return messages
    
    def get_chatgpt_response(messages, model=model):
        response = openai.ChatCompletion.create(
        model=model,
        messages=messages
        )
        return response['choices'][0]['message']['content']

   # def fixed_response(generated_response):
  #      string = generated_response
   #     string = " ".join(string.split())
   #     return string
    
    def update_chat(messages, role, content):
        messages.append({"role": role, "content": content})
        return messages


    st.title(":male-teacher: Professor Virtual")
    st.write('Selecionou:', option)

    # Armazenando a sessão 

    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
        
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    
    query = st.text_input("Questão: ", "", key="input")

    if 'messages' not in st.session_state:
        st.session_state['messages'] = get_initial_message()

    if query:
        with st.spinner("generating..."):
            messages = st.session_state['messages']
            messages = update_chat(messages, "user", query)
            response = get_chatgpt_response(messages, model)
            messages = update_chat(messages, "assistant", response)
            st.session_state.past.append(query)
            st.session_state.generated.append(response)

        
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i), avatar_style= "open-peeps")
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

    
    def clear_chat() -> None:
        st.session_state.generated = []
        st.session_state.past = []
        st.session_state.messages = []
        st.session_state.user_text = ""


    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


if authentication_status is False:
    st.error('Username/password incorrecto')


if authentication_status is None:
    st.warning('Por favor insira o seu username e password')

hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 