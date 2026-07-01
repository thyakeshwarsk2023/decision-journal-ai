from services.memory_service import (
    store_memory,
    retrieve_memories
)


store_memory(
    "1",
    "I want to switch to machine learning."
)

store_memory(
    "2",
    "I am afraid of placements."
)

store_memory(
    "3",
    "I love playing football."
)


results = retrieve_memories(
    "Should I pursue AI?"
)

print(results["documents"])