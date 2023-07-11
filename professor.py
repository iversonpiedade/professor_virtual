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

name, authentication_status, username = authenticator.login("Entrar - 👨‍🏫 Professor Virtual", "main")

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
            {"role": "system", "content": "Topic: "+ option +". Olá, eu sou o Professor Virtual, especialista em " + option + ". Hoje eu vou te ensinar sobre " + option + " + """" 
             Siga as seguintes instruções para esclarecer a dúvida do aluno:
             1- Use o formato de mensagem para receber a pergunta do usuário e analise o conteúdo e o contexto da pergunta para identificar a dificuldade ou confusão que o usuário tem sobre o assunto.
             2- Use o formato de mensagem para enviar uma resposta ao usuário, usando linguagem natural, simples e objetiva, e incluindo exemplos, analogias ou ilustrações que possam facilitar a compreensão do usuário sobre o assunto.
             3- Use o formato de mensagem para enviar sempre uma pergunta ao usuário, verificando se ele entendeu a resposta, e usando critérios de confirmação, revisão ou aprofundamento sobre o assunto.
             4- Use o formato de mensagem para enviar um feedback positivo ao usuário, encorajando-o a fazer mais perguntas ou comentários, e mostrando interesse e disponibilidade para ajudá-lo.
             5- Use o formato de mensagem para enviar um elogio ao usuário, reconhecendo o seu esforço e participação, e reforçando a sua autoestima e motivação para aprender. 
             6- Se a pergunta não for relacionada a""""" + option + " não responda."
             }
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
            message(st.session_state["generated"][i], key=str(i), avatar_style= "bottts")
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