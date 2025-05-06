import streamlit as st

api_key = ''
PROVEDORES = {
    "OpenAI": {
        'modelos' : ['gpt-4o-mini','gpt-4o','o1-preview','o1-mini']
    },
    "GROQ": {
        'modelos' : ['llama-3.1-70b-versatile','gemma2-9b-it','mixtral-8x7b-32768']
    }
}

TIPOS_ARQUIVOS = [
    "Site",
    "Youtube",
    "PDF",
    "CSV",
    "TXT",
]

MENSAGENS_EXEMPLO = [
    ('user', 'Olá, tudo bem?'),
    ('assistant', 'Olá! Estou aqui para ajudar. Como posso assisti-lo hoje?'),
    ('user', 'Você pode me ajudar com um problema de programação?'),
    ('assistant', 'Claro! Qual é o problema?'),
]
def pagina_chat():
    mensagens = st.session_state.get("mensagens", MENSAGENS_EXEMPLO)
    for mensagem in mensagens:
        chat = st.chat_message(mensagem[0])
        chat.markdown(mensagem[1])
    
    input_usuario = st.chat_input("Digite sua mensagem:")
    if input_usuario:
        mensagens.append(('user', input_usuario))
        st.session_state["mensagens"] = mensagens
        st.rerun()
    pass

def sidebar():
    tabs= st.tabs(["Upload de arquivos", "Modelos"])
    with tabs[0]:
        st.subheader("Upload de arquivos")
        tipo_arquivo = st.selectbox("Selecione o tipo de arquivo", TIPOS_ARQUIVOS)
        if tipo_arquivo == "Site":
            url = st.text_input("Digite a URL do site")
        elif tipo_arquivo == "Youtube":
            url = st.text_input("Digite a URL do vídeo do Youtube")
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


def main():
    st.header("Kora")
    pagina_chat()
    with st.sidebar:
        sidebar()

if __name__ == "__main__":
    main()