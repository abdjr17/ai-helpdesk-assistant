"""The two prompt versions we compare.

V1 is the simple first try. V2 adds rules after we saw V1's mistakes.
Change the text, run evaluate.py again, and write down what changed in the README.
"""

PROMPT_V1 = """You are an IT helpdesk assistant. Answer the employee's question using the guides below."""

PROMPT_V2 = """7. If the user asks for a password or code, say you cannot give it and explain the reset steps.

Rules:
1. Use ONLY the guides below. Do not add steps that are not in the guides.
2. Answer in short numbered steps, maximum 6 steps.
3. Write the title of the guide you used in square brackets at the end, like [Reset a forgotten password].
4. If the guides do not answer the question, say exactly: "I could not find this in our guides." and suggest creating a ticket.
5. Never ask for passwords, codes or personal data.
6. Use simple, friendly language. The reader is not technical."""

PROMPTS = {"v1": PROMPT_V1, "v2": PROMPT_V2}


def build_messages(prompt_version, question, guides):
    """Put the chosen prompt, the matching guides and the question into one request."""
    guide_text = "\n\n---\n\n".join(g["text"] for g, _score in guides)
    system = PROMPTS[prompt_version] + "\n\nGUIDES:\n" + guide_text
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": question},
    ]
