import json
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def load_docs(path: str):
    with open(path, "r") as f:
        data = json.load(f)

    docs = []
    for item in data:
        docs.append(Document(page_content=item))
    return docs


def build_retriever(json_path: str):
    docs = load_docs(json_path)
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    store = FAISS.from_documents(docs, embeddings)
    return store.as_retriever(search_kwargs={"k": 3})


def load_retrievers():
    return {
        "failures": build_retriever("app/data/failures.json"),
        "causes": build_retriever("app/data/root_causes.json"),
        "fixes": build_retriever("app/data/fixes.json"),
    }
