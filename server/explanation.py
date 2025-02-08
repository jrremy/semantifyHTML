from openai import OpenAI
from typing import Optional
import redis

def generate_explanation_stream(original_tag: str, new_tag: str, openai_client: Optional[OpenAI], redis_client: Optional[redis.StrictRedis], redis_available: bool):
    """
    Generates an explanation for the change from original_tag to new_tag.
    Streams the explanation to the client and caches it in Redis if available.
    """
    prompt = (
        f"The HTML tag '{original_tag}' was changed to '{new_tag}'. "
        f"Explain the purpose and specific function of the '{new_tag}' tag in HTML, including its impact on semantics, accessibility, and SEO. "
        f"Provide a concise and clear explanation, no more than a couple complete sentences."
    )

    # Check Redis cache first
    if redis_available:
        cache_key = f"{original_tag}:{new_tag}"
        cached_explanation = redis_client.get(cache_key)
        if cached_explanation:
            yield cached_explanation.decode('utf-8')
            return

    try:
        # Generate explanation using OpenAI
        stream = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            stream=True
        )
        # Stream explanation as chunks
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

        # Cache the explanation if Redis is available
        if redis_available:
            redis_client.set(cache_key, chunk.choices[0].delta.content)

    except Exception as e:
        yield f"Error: {str(e)}"
