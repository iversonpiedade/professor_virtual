# Importando as libraries 

import openai 
import streamlit as st
from streamlit_chat import message 

st.set_page_config(
    page_title="Professor Virtual",
    page_icon="👩🏿‍🏫"
)

openai.api_key = st.secrets["api_secret"]


# Função que fará a geração de chamadas da API

def generate_response(prompt):
    completations = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = "És um professor virtual com o objectivo de esclarecer dúvidas. Você: Olá, serei o teu professor virtual daqui para frente, em que posso ajudar? Aluno:" + prompt, 
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