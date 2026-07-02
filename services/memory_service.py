import chromadb

from services.embedding_service import embed_text

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="decision_memories"
)

def store_decision_memory(
        decision_id: int,
        title: str,
        decision_text: str,
        user_id: int,
):
    full_text = f"""
Title: {title}
Decision Text: {decision_text}
"""    
    embedding = embed_text(full_text)
    collection.add(
        ids=[
            f"decision_{decision_id}"
        ],
        documents=[
            full_text
        ],
        embeddings=[
            embedding
        ],

        metadatas=[{
            "user_id": user_id,
            "decision_id": decision_id,
            "type": "decision"
        }]
    )

def retrieve_similar_decisions(
        query: str,
        user_id: int,
        n_results: int = 3
):
    query_embedding = embed_text(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,

        where={
            "user_id": user_id
        }
    )
    return results

def delete_memory(
        decision_id: int
):
    collection.delete(
        ids=[f"decision_{decision_id}"]
    )
