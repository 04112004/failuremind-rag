import os
import json
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

BASE_DIR = os.path.dirname(__file__)

def load_docs(filename):
    path = os.path.join(BASE_DIR, "data", filename)
    with open(path, "r") as f:
        data = json.load(f)

    # data is a list of strings
    return [Document(page_content=item) for item in data]

def build_retriever(filename):
    docs = load_docs(filename)
    return FAISS.from_documents(docs, embeddings).as_retriever(
        search_kwargs={"k": 2}
    )

def load_retrievers():
    return {
        "failures": build_retriever("failures.json"),
        "causes": build_retriever("root_causes.json"),
        "fixes": build_retriever("fixes.json"),
    }

