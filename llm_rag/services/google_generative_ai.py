from django.conf import settings
from google import genai
from google.genai import types

GEMINI_API_KEY = settings.GEMINI_API_KEY


def get_client():
    return genai.Client(api_key=GEMINI_API_KEY)


def get_embeddings(texts):
    client = get_client()
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=texts,
        config=types.EmbedContentConfig(output_dimensionality=768),
    )
    return [e.values for e in response.embeddings]


def llm_gemini_2_5_flash(prompt):
    client = get_client()
    print("Request is sending to AI")
    return client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
