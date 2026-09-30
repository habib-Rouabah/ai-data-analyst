from groq import Groq

from src.config import settings

_client = None


def get_client():
    global _client
    if _client is None:
        if not settings.groq_api_key:
            raise RuntimeError("GROQ_API_KEY is missing. Set it in your .env file.")
        _client = Groq(api_key=settings.groq_api_key)
    return _client


def complete(system, user):
    client = get_client()
    response = client.chat.completions.create(
        model=settings.llm_model,
        temperature=settings.temperature,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return response.choices[0].message.content
