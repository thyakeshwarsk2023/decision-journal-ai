from services.memory_service import(
    retrieve_similar_decisions,
)

def build_memory_context(
        decision_text: str,
        user_id: int
):
    results = retrieve_similar_decisions(
        query=decision_text,
        user_id=user_id,
        n_results=3
    )

    documents = results['documents'][0]
    if not documents:
        return "No relevant memories found."
    
    context = "\n\n".join(
        f"Past Memory:\n{doc}"
        for doc in documents
    )

    return context
