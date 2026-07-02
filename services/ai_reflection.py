from services.local_llm import generate_response
from services.bias_engine import COGNITIVE_BIASES
from services.mental_models import MENTAL_MODELS
from services.rag_service import (
    build_memory_context
)
def generate_ai_reflection(
    decision_text: str,
    reflections: list[str],
    user_id: int
)-> str:
     reflection_text = "\n".join(reflections)
     memory_context = build_memory_context(
          decision_text,
          user_id
     )
     biases = "\n".join(
        f"- {bias.replace('_',' ').title()}"
        for bias in COGNITIVE_BIASES.keys()
     )

     mental_models = "\n".join(
        f"- {model.replace('_', ' ').title()}"
        for model in MENTAL_MODELS.keys()
     )
     

     prompt = f"""
You are an expert in:

- Psychology
- Decision Science
- Behavioral Economics
- Critical Thinking
- Mental Models

Relevant Past Experiences:
{memory_context}

Analyze the user's decision using the following cognitive biases:
{biases}

Use the following mental models where appropriate:
{mental_models}

Current Decision:
{decision_text}

User Reflections:
{reflection_text}

Provide:

1. Short summary
2. Possible cognitive biases affecting the decision.
3.Relevant mental models that should be applied.
4. Alternative viewpoints.
5.Long-term consequences and second-order effects.
6. Two powerful questions for future reflection

Focus on improving the quality of the decision-making process rather than merely judging the outcome.

Keep the response concise, practical and intellectually honest.
"""
     return generate_response(prompt)