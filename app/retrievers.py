import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import VECTOR_DIR, EMBED_MODEL

embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

def safe_load(path: str):
    if not os.path.exists(path):
        print(f"[WARN] Vectorstore missing: {path}")
        return None

    return FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True
    ).as_retriever(search_kwargs={"k": 2})


def load_retrievers():
    return {
        "failures": safe_load(f"{VECTOR_DIR}/failures"),
        "causes": safe_load(f"{VECTOR_DIR}/causes"),
        "fixes": safe_load(f"{VECTOR_DIR}/fixes"),
    }
