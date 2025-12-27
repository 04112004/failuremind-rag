from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import VECTOR_DIR, EMBED_MODEL

embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

def load_retrievers():
    retrievers = {}

    for name in ["failures", "causes", "fixes"]:
        path = Path(VECTOR_DIR) / name

        if (path / "index.faiss").exists():
            retrievers[name] = FAISS.load_local(
                path,
                embeddings,
                allow_dangerous_deserialization=True
            ).as_retriever(search_kwargs={"k": 2})
        else:
            retrievers[name] = None  # 🔑 IMPORTANT

    return retrievers
