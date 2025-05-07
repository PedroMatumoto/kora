from langchain_community.document_loaders import WebBaseLoader, YoutubeLoader, PyPDFLoader, CSVLoader, TextLoader
from fake_useragent import UserAgent
import os
import streamlit as st
from time import sleep

def load_site(url):
    document = ''
    for i in range(5):
        try:
            os.environ["USER_AGENT"] = UserAgent().random
            loader = WebBaseLoader(url, raise_for_status=True)
            documents = loader.load()
            document = '\n\n'.join([doc.page_content for doc in documents])
            break
        except Exception as e:
            print(f"Erro ao carregar o site: {e}")
            sleep(3)
    if document == '':
        st.error("Erro ao carregar o site. Verifique a URL e tente novamente.")
        st.stop()
    return document

def youtube_loader(id_video):
    loader = YoutubeLoader.from_youtube_url(id_video, add_video_info=False, language="pt")
    documents = loader.load()
    document = '\n\n'.join([doc.page_content for doc in documents])
    return document

def carrega_csv(arquivo):
    loader = CSVLoader(file=arquivo)
    documents = loader.load()
    document = '\n\n'.join([doc.page_content for doc in documents])
    return document

def carrega_pdf(arquivo):
    loader = PyPDFLoader(file=arquivo)
    documents = loader.load()
    document = '\n\n'.join([doc.page_content for doc in documents])
    return document

def carrega_txt(arquivo):
    loader = TextLoader(file=arquivo)
    documents = loader.load()
    document = '\n\n'.join([doc.page_content for doc in documents])
    return document

