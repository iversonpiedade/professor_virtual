# Importando as bibliotecas 
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import openai 
import streamlit as st
from streamlit_chat import message 
import database as db 


st.set_page_config(
    page_title="Professor Virtual",
    page_icon=":man_teacher:"
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

authenticator = stauth.Authenticate(credentials, "professor_virtual", "abcdef", cookie_expiry_days=0)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status  == True:
    authenticator.logout('Sair da Conta', 'main', key='unique_key')
    st.write(f'Olá *{name}*, em que disciplina precisa de ajuda hoje?')
    option = st.selectbox(
            '',
            ('TIC', 'Matemática', "EDP", ""))
    
    openai.api_key = st.secrets["api_secret"]
    
    # Função que fará a geração de chamadas da API
    def generate_response(prompt):
        completations = openai.Completion.create(
            engine = "text-davinci-003",
            prompt = "És um professor virtual especialista em *{option}* com o objectivo de esclarecer dúvidas e guiar o aluno à solução. Você: Olá, serei o teu professor virtual daqui para frente, qual é a sua dúvida em *{option}*? Aluno:" + prompt, 
            max_tokens = 1024,
            n = 1,
            stop = None, 
            temperature = 0.5, 
            )
        
        message = completations.choices[0].text
        return message

    def fixed_response(generated_response):
        string = generated_response
        string = " ".join(string.split())
        return string


    st.title("👩🏿‍🏫 Professor Virtual")
    st.write('You selected:', option)
    # Armazenando a sessão 

    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    def get_text():
        input_text = st.text_input("Você:", key="input")
        return input_text 

    user_input = get_text()

        
    if user_input:
        output = generate_response(user_input)
        fixed = fixed_response(output)
        print(fixed)
        # Armazena a saída 
        st.session_state.past.append(user_input)
        st.session_state.generated.append(fixed)

    if st.session_state["generated"]: 
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


if authentication_status is False:
    st.error('Username/password is incorrect')


if authentication_status is None:
    st.warning('Please enter your username and password')

hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 