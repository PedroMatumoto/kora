import tempfile
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from docs_imports import *
api_key = ''
PROVEDORES = {
    "OpenAI": {
        'modelos' : ['gpt-4o-mini','gpt-4o','o1-preview','o1-mini'],
        'chat' : ChatOpenAI
    },
    "GROQ": {
        'modelos' : ['llama-3.1-70b-versatile','gemma2-9b-it','mixtral-8x7b-32768'],
        'chat' : ChatGroq
    }
}

TIPOS_ARQUIVOS = [
    "Site",
    "Youtube",
    "PDF",
    "CSV",
    "TXT",
]

MEMORIA = ConversationBufferMemory()

def carrega_arquivos(file_type, file):
    if file_type == "Site":
        document = load_site(file)
    elif file_type == "Youtube":
        document = youtube_loader(file)
    elif file_type == "PDF":
        with tempfile.NamedTemporaryFile(suffix=".pdf",delete=False) as tmp:
            tmp.write(file.read())
            nome_temp = tmp.name
        document = carrega_pdf(nome_temp)
    elif file_type == "CSV":
        document = carrega_csv(file)
    elif file_type == "TXT":
        document = carrega_txt(file)
    else:
        st.error("Tipo de arquivo não suportado.")
        return
    st.session_state["document"] = document

def carrega_modelo(provedor, modelo, api_key, tipo_arquivo, arquivo):
    documento = carrega_arquivos(tipo_arquivo, arquivo)

    template = ChatPromptTemplate.from_messages([
        ("system", "Você é um assistente que se chama Kora, e está aqui para ajudar o usuário a encontrar informações em documentos."),
        ("system", "Você pode fazer perguntas ao usuário para entender melhor o que ele precisa."),
        ("system", "Você deve responder de forma clara e objetiva."),
        ("system", "O tipo do documento é {tipo_arquivo}"),
        ("system", "Você tem acesso a um documento que contém as seguintes informações: {documento}"),
        ("system", "Você deve usar essas informações para responder às perguntas do usuário."),
        ("system", "Se houver $ na resposta, troque por S"),
        ("system", "Se você não souber a resposta, diga que não sabe."),
        ("placeholder", '{chat_history}'),
        ("user", "{input}"),
    ])



    chat = PROVEDORES[provedor]['chat'](model=modelo, api_key=api_key)
    chain = template | chat
    st.session_state["chain"] = chain

def pagina_chat():
    chain = st.session_state.get("chain")
    if chain is None:
        st.error("Por favor, carregue um modelo na barra lateral.")
        return
    memoria = st.session_state.get("memoria", MEMORIA)
    for mensagem in memoria.buffer_as_messages:
        chat = st.chat_message(mensagem.type)
        chat.markdown(mensagem.content)
    
    input_usuario = st.chat_input("Digite sua mensagem:")
    if input_usuario:
        memoria.chat_memory.add_user_message(input_usuario)
        chat = st.chat_message('human')
        chat.markdown(input_usuario)

        chat = st.chat_message('ai')
        resposta = chat.write_stream(chain.stream({
            "input": input_usuario,
            "tipo_arquivo": st.session_state.get("tipo_arquivo"),
            "documento": st.session_state.get("document"),
            "chat_history": memoria.buffer_as_messages,
        }))
        memoria.chat_memory.add_ai_message(resposta)
        st.session_state["memoria"] = memoria
    pass

def sidebar():
    tabs= st.tabs(["Upload de arquivos", "Modelos"])
    with tabs[0]:
        st.subheader("Upload de arquivos")
        tipo_arquivo = st.selectbox("Selecione o tipo de arquivo", TIPOS_ARQUIVOS)
        if tipo_arquivo == "Site":
            arquivo = st.text_input("Digite a URL do site")
        elif tipo_arquivo == "Youtube":
            arquivo = st.text_input("Digite a URL do vídeo do Youtube")
        elif tipo_arquivo == "PDF":
            arquivo = st.file_uploader("Carregue seu arquivo PDF", type="pdf")
            if arquivo is not None:
                st.success(f"Arquivo {arquivo.name} enviado com sucesso!")
        elif tipo_arquivo == "CSV":
            arquivo = st.file_uploader("Carregue seu arquivo CSV", type="csv")
            if arquivo is not None:
                st.success(f"Arquivo {arquivo.name} enviado com sucesso!")
        elif tipo_arquivo == "TXT":
            arquivo = st.file_uploader("Carregue seu arquivo TXT", type="txt")
            if arquivo is not None:
                st.success(f"Arquivo {arquivo.name} enviado com sucesso!")
    with tabs[1]:
        provedor = st.selectbox("Selecione o provedor", PROVEDORES.keys())
        modelo = st.selectbox("Selecione o modelo", PROVEDORES[provedor]['modelos'])

    if st.button("Carregar modelo", use_container_width=True):
        carrega_modelo(provedor, modelo, api_key, tipo_arquivo, arquivo)
    


def main():
    st.header("Kora")
    with st.sidebar:
        sidebar()
    pagina_chat()

if __name__ == "__main__":
    main()