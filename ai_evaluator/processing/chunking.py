# processing/chunking.py
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_data(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    chunks = []
    for doc in documents:
        splits = splitter.split_text(doc["content"])
        for s in splits:
            chunks.append({
                "source": doc["source"],
                "content": s
            })

    return chunks