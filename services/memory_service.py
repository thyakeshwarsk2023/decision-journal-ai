import chromadb

from services.embedding_service import embed_text

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="decision_memories"
)

def store_memory(
        memory_id: str,
        text: str
):
    embedding = embed_text(text)
    collection.add(
        ids=[memory_id],
        documents=[text],
        embeddings=[embedding]
    )

def retrieve_memories(
        query: str,
        n_results: int = 3
):
    query_embedding = embed_text(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results

