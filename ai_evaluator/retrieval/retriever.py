# retrieval/retriever.py

def retrieve_evidence(vector_store, query, k=5):
    """
    Retrieve top-k relevant evidence chunks

    Returns:
    - content
    - source
    - type
    """

    docs = vector_store.similarity_search(query, k=k)

    results = []

    for d in docs:
        results.append({
            "content": d.page_content,
            "source": d.metadata.get("source"),
            "type": d.metadata.get("type"),
            "file_path": d.metadata.get("file_path"),
            "timestamp": d.metadata.get("timestamp")
        })

    return results