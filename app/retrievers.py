import json
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from app.config import EMBED_MODEL

embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

def load_docs(path):
    with open(path, "r") as f:
        data = json.load(f)
    return [Document(page_content=item) for item in data]

def build_retriever(json_path):
    docs = load_docs(json_path)
    store = FAISS.from_documents(docs, embeddings)
    return store.as_retriever(search_kwargs={"k": 2})

def load_retrievers():
    return {
        "failures": build_retriever("data/failures.json"),
        "causes": build_retriever("data/root_causes.json"),
        "fixes": build_retriever("data/fixes.json"),
    }

