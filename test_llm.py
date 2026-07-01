from services.local_llm import generate_response

response = generate_response(
    "Explain opportunity cost in one sentence."
)

print(response)