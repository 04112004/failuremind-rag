import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import VECTOR_DIR, EMBED_MODEL

embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

def safe_load(name: str):
    path = os.path.join(VECTOR_DIR, name)
    if not os.path.exists(path):
        print(f"[WARN] Vectorstore missing: {path}")
        return None

    try:
        return FAISS.load_local(
            path,
            embeddings,
            allow_dangerous_deserialization=True
        ).as_retriever(search_kwargs={"k": 2})
    except Exception as e:
        print(f"[ERROR] Failed loading {name}: {e}")
        return None

def load_retrievers():
    return {
        "failures": safe_load("failures"),
        "causes": safe_load("causes"),
        "fixes": safe_load("fixes"),
    }
