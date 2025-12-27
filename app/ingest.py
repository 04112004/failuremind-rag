import json, os
from langchain_community.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from config import DATA_DIR, VECTOR_DIR, EMBED_MODEL

os.makedirs(VECTOR_DIR, exist_ok=True)

embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

def load_json(file):
    with open(file, "r") as f:
        return json.load(f)

def to_docs(items, builder):
    return [Document(page_content=builder(i)) for i in items]

def ingest():
    failures = load_json(f"{DATA_DIR}/failures.json")
    causes = load_json(f"{DATA_DIR}/root_causes.json")
    fixes = load_json(f"{DATA_DIR}/fixes.json")

    failure_docs = to_docs(
        failures,
        lambda f: f"Failure in {f['system_type']} during {f['stage']}: "
                  f"{f['description']} Impact: {f['impact']}"
    )

    cause_docs = to_docs(
        causes,
        lambda c: f"Root cause: {c['root_cause']}. Why: {c['why']}. "
                  f"Signals: {', '.join(c['signals'])}"
    )

    fix_docs = to_docs(
        fixes,
        lambda m: f"Solution: {m['solution']}. "
                  f"Tools: {', '.join(m['tools'])}"
    )

    FAISS.from_documents(failure_docs, embeddings).save_local(f"{VECTOR_DIR}/failures")
    FAISS.from_documents(cause_docs, embeddings).save_local(f"{VECTOR_DIR}/causes")
    FAISS.from_documents(fix_docs, embeddings).save_local(f"{VECTOR_DIR}/fixes")

if __name__ == "__main__":
    ingest()
