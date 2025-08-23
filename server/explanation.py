from openai import OpenAI
from typing import Optional, Generator
import redis
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_explanation_stream(
    original_tag: str, 
    new_tag: str, 
    openai_client: Optional[OpenAI], 
    redis_client: Optional[redis.Redis], 
    redis_available: bool
) -> Generator[str, None, None]:
    """
    Generates an explanation for the change from original_tag to new_tag.
    Streams the explanation to the client and caches it in Redis if available.
    
    Args:
        original_tag: The original HTML tag that was changed
        new_tag: The new semantic HTML tag
        openai_client: OpenAI client instance
        redis_client: Redis client instance for caching
        redis_available: Whether Redis is available for caching
        
    Yields:
        str: Chunks of the explanation as they are generated
    """
    
    if not openai_client:
        yield "Error: OpenAI client not available. Please check your API key configuration."
        return
    
    # Specific prompt focusing on the individual tag's purpose
    prompt = f"""The HTML tag '{original_tag}' was changed to '{new_tag}'.

Explain specifically what the '{new_tag}' tag does and its unique purpose in HTML. Focus on what makes this tag different from a generic div and why it's more meaningful for this particular content.

Keep it concise (2-3 sentences max) and avoid generic statements about semantic HTML benefits. Be brief but complete."""

    # Check Redis cache first
    cache_key = f"explanation:{original_tag}:{new_tag}"
    if redis_available and redis_client:
        try:
            cached_explanation = redis_client.get(cache_key)
            if cached_explanation:
                logger.info(f"Cache hit for {cache_key}")
                yield cached_explanation.decode('utf-8')
                return
        except Exception as e:
            logger.warning(f"Redis cache error: {e}")
            # Continue without caching if Redis fails

    try:
        # Try to use the latest model, fallback to older ones if needed
        models_to_try = [
            "gpt-4o-mini",         # Latest and most cost-effective
            "gpt-3.5-turbo-0125",  # Latest 3.5 model
            "gpt-3.5-turbo"        # Fallback
        ]
        
        stream = None
        used_model = None
        
        for model in models_to_try:
            try:
                logger.info(f"Attempting to use model: {model}")
                stream = openai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You provide specific, tag-focused explanations. Avoid generic statements about semantic HTML benefits. Focus on what each tag uniquely does and why it's better than a div for that specific content."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=150,  # Increased to ensure complete explanations
                    temperature=0.3, # Balanced temperature for good responses
                    stream=True
                )
                used_model = model
                logger.info(f"Successfully using model: {model}")
                break
            except Exception as e:
                logger.warning(f"Failed to use model {model}: {e}")
                continue
        
        if not stream:
            yield "Error: Unable to connect to OpenAI API. Please check your API key and internet connection."
            return
        
        # Stream explanation as chunks and collect full response for caching
        full_explanation = ""
        chunk_count = 0
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_explanation += content
                chunk_count += 1
                yield content

        # Cache the full explanation if Redis is available and we got a response
        if redis_available and redis_client and full_explanation:
            try:
                # Cache for 24 hours (86400 seconds)
                redis_client.setex(cache_key, 86400, full_explanation)
                logger.info(f"Cached explanation for {cache_key} using model {used_model}")
            except Exception as e:
                logger.warning(f"Failed to cache explanation: {e}")

    except Exception as e:
        logger.error(f"Error generating explanation: {e}")
        yield f"Error generating explanation: {str(e)}"
        yield "\n\nPlease check your OpenAI API key and ensure you have sufficient credits."
