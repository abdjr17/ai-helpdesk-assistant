# AI Helpdesk Assistant

A small Python assistant that answers first-level IT support questions from a set of short fix guides, logs every question as a ticket, and escalates to a human when it has no answer. I built it to practise prompt engineering, LLM API integration, testing and documentation.

>    > **Status:** working version. The prompt comparison and test results are being added.
## What it does

1. An employee asks an IT question in the terminal.
2. Personal data (emails, phone numbers, IBANs) is removed from the question before anything is sent to an AI service.
3. A simple keyword search finds the best matching guides (no AI needed for this step).
4. The matching guides and the question are sent to an LLM with strict rules ("use only these guides").
5. The answer is shown with its sources. If no guide matches, the AI is **not** called: the assistant says so and creates a ticket.

```
Question -> remove personal data -> find guides -> LLM with rules -> answer + sources
                                         |
                                  no guide found -> ticket for a human
```

## Tech

Python 3, `openai` package (works with OpenAI, Google Gemini or a local Ollama model by changing 3 settings), `python-dotenv`. No framework, about 200 lines of code.

## Run it

```bash
git clone <your-repo-url>
cd ai-helpdesk-assistant
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then edit .env (see below)
python src/helpdesk.py
```

- `LLM_MODE=mock` runs without an API key and returns fake answers (to test the program).
- `LLM_MODE=live` needs `LLM_API_KEY`, `LLM_BASE_URL` and `LLM_MODEL` in `.env`.



## Testing

- 20 test questions in `tests/test_questions.csv`: 17 questions with a known correct guide and 3 questions that are **not** covered (the assistant must not invent an answer).
- `python evaluate.py` runs everything and writes `results/results.csv`.
- Test plan and results: see `docs/test_plan.md`.

**Guide matching result:** [fill in, e.g. 18/20 correct]

**Error analysis (the questions it got wrong):**
- [question] -> found [guide], expected [guide]. Reason: [why]. Fix idea: [what you would change]
- [question] -> ...

## Data protection

- Emails, phone numbers and IBANs are replaced by `[EMAIL]`, `[NUMBER]`, `[IBAN]` before a question is sent to the AI service and before it is saved in a ticket.
- The assistant is instructed never to ask for passwords or codes.
- `.env` (the API key) is in `.gitignore` and is never committed.
- Limits: the redaction is simple pattern matching. It does not find names or addresses. A real system would need more.

## Limitations and next steps

- Keyword matching is simple. Next step: semantic search with embeddings.
- Only English guides. Next step: German guides and questions.
- Terminal only. Next step: small web interface (Streamlit).
- Answers are only as good as the guides. Next step: a feedback button ("Did this solve it?") and a monthly review of escalated tickets.


