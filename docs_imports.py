from langchain_community.document_loaders import WebBaseLoader, YoutubeLoader, PyPDFLoader, CSVLoader, TextLoader

def load_site(url):
    loader = WebBaseLoader(url)
    documents = loader.load()
    document = '\n\n'.join([doc.page_content for doc in documents])
    return document

def youtube_loader(id_video):
    loader = YoutubeLoader.from_youtube_url(url, add_video_info=False, language="pt")
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

