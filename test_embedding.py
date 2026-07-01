from services.embedding_service import embed_text

v = embed_text(
    "I am afraid of switching to ML."
)

print("Dimensions:", len(v))
print("First 10 values:")
print(v[:10])