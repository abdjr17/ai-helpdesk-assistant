"""AI helpdesk assistant - run this file to chat in the terminal.

    python src/helpdesk.py

Type your IT question. Type 'ticket' to escalate the last question to a human.
Type 'quit' to leave.
"""
from retriever import load_guides, retrieve
from prompts import build_messages
from llm import ask_llm
from safety_and_tickets import redact, log_ticket

PROMPT_VERSION = "v2"
FALLBACK = "I could not find this in our guides."


def answer_question(question, guides, prompt_version=PROMPT_VERSION):
    """Return (answer, matching_guides). Never calls the AI if no guide matches."""
    safe_question = redact(question)  # remove personal data first
    matches = retrieve(safe_question, guides)
    if not matches:
        return FALLBACK, []
    messages = build_messages(prompt_version, safe_question, matches)
    return ask_llm(messages, matches), matches


def main():
    guides = load_guides()
    print(f"IT Helpdesk Assistant ready. {len(guides)} guides loaded.")
    print("Ask a question. Type 'ticket' to escalate, 'quit' to leave.\n")
    last_question = None

    while True:
        question = input("You: ").strip()
        if not question:
            continue
        if question.lower() == "quit":
            break
        if question.lower() == "ticket":
            if last_question:
                ticket_id = log_ticket(redact(last_question), "escalated")
                print(f"Assistant: Ticket #{ticket_id} created for the IT team.\n")
            else:
                print("Assistant: Ask a question first.\n")
            continue

        last_question = question
        answer, matches = answer_question(question, guides)
        print(f"\nAssistant: {answer}")
        if matches:
            print("Sources:", ", ".join(g["title"] for g, _ in matches))
            log_ticket(redact(question), "answered", matches[0][0]["title"])
        else:
            ticket_id = log_ticket(redact(question), "escalated")
            print(f"Ticket #{ticket_id} created for the IT team.")
        print()


if __name__ == "__main__":
    main()
