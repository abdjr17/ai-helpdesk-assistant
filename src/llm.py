"""Talks to the language model (LLM).

LLM_MODE=mock  -> no internet, no key. Returns a fake answer. Good for testing the code.
LLM_MODE=live  -> sends the request to the provider set in the .env file.
"""
import os
from dotenv import load_dotenv

load_dotenv()


def ask_llm(messages, guides):
    mode = os.getenv("LLM_MODE", "mock").lower()

    if mode == "mock":
        title = guides[0][0]["title"] if guides else "no guide"
        return f"[MOCK ANSWER] I would answer using the guide: {title}"

    from openai import OpenAI

    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL") or None
    model = os.getenv("LLM_MODEL")
    if not api_key or not model:
        return "[ERROR] Please set LLM_API_KEY and LLM_MODEL in your .env file."

    client = OpenAI(api_key=api_key, base_url=base_url, timeout=90, max_retries=1)
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2,  # low = more stable, less creative answers
            max_tokens=2000,
        )
        choice = response.choices[0]
        text = (choice.message.content or "").strip()
        if not text:
            return f"[ERROR] The AI returned an empty answer (finish reason: {choice.finish_reason})."
        return text
    except Exception as error:  # show a friendly message instead of a long error
        return f"[ERROR] The AI service did not answer: {error}"