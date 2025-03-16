from langchain.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
CHROMA_STORE = 'chroma'
def get_info_chroma(query):
    embedding_model = OllamaEmbeddings(model = 'qwen2.5:7b')
    docsearch = Chroma(embedding_function=embedding_model, collection_name="docx_files", persist_directory=CHROMA_STORE)
    results = docsearch.similarity_search(query, k=5)
    return {idx: result.page_content for idx, result in enumerate(results)}