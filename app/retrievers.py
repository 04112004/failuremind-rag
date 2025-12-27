from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import VECTOR_DIR, EMBED_MODEL


embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

def load_retrievers():
    return {
        "failures": FAISS.load_local(
            f"{VECTOR_DIR}/failures",
            embeddings,
            allow_dangerous_deserialization=True
        ).as_retriever(search_kwargs={"k": 2}),

        "causes": FAISS.load_local(
            f"{VECTOR_DIR}/causes",
            embeddings,
            allow_dangerous_deserialization=True
        ).as_retriever(search_kwargs={"k": 2}),

        "fixes": FAISS.load_local(
            f"{VECTOR_DIR}/fixes",
            embeddings,
            allow_dangerous_deserialization=True
        ).as_retriever(search_kwargs={"k": 2}),
    }
