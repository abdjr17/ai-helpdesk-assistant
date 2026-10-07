# Test plan

## Goal
Check that the assistant (1) finds the right guide, (2) gives correct and clear steps, (3) does not invent answers for questions outside the guides, and (4) hides personal data.

## Test data
- `tests/test_questions.csv`: 20 questions. 17 have an expected guide. 3 are out of scope (`NONE`).

## Method
1. Run `python evaluate.py` with `LLM_MODE=live`.
2. Open `results/results.csv`.
3. For each question, read `answer_v1` and `answer_v2` and give a score by hand:
   - 0 = wrong or made-up steps
   - 1 = partly right
   - 2 = correct and clear
4. Fill the table below and copy the totals into the README.

## Test cases

| ID | What is tested | Input | Expected | Actual | Pass? |
|----|----------------|-------|----------|--------|-------|
| T1 | Right guide found | "I forgot my password and cannot log in" | guide: Reset a forgotten password | [fill in] | [ ] |
| T2 | Out-of-scope question | "What is the capital of France?" | "I could not find this in our guides." + ticket | [fill in] | [ ] |
| T3 | Personal data removed | "Call me on 0176 12345678, mail max@test.de" | `[NUMBER]` and `[EMAIL]` in the ticket | [fill in] | [ ] |
| T4 | No invented steps | Ask a question and compare the steps with the guide | every step exists in the guide | [fill in] | [ ] |
| T5 | Escalation | type `ticket` after a question | a new row in `data/tickets.csv` | [fill in] | [ ] |
| T6 | Missing API key | live mode without key | clear error message | [fill in] | [ ] |

## Results summary

| Measure | v1 | v2 |
|---------|----|----|
| Guide found correctly | [x/20] | [x/20] |
| Total answer score (max 34) | [fill in] | [fill in] |
| Out-of-scope questions answered correctly with "could not find" (max 3) | [fill in] | [fill in] |

## Known problems
- [write the wrong cases and what you would change]
