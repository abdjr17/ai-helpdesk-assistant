"""Runs every test question with prompt v1 and prompt v2 and saves the results.

    python evaluate.py

Open results/results.csv afterwards and fill the v1_score and v2_score columns by hand:
    0 = wrong or made-up, 1 = partly right, 2 = correct and clear
Then copy the totals into the README.
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from retriever import load_guides, retrieve      # noqa: E402
from prompts import build_messages               # noqa: E402
from llm import ask_llm                          # noqa: E402
from helpdesk import FALLBACK                    # noqa: E402

TESTS = Path(__file__).parent / "tests" / "test_questions.csv"
RESULTS = Path(__file__).parent / "results" / "results.csv"


def main():
    guides = load_guides()
    rows = []
    with open(TESTS, encoding="utf-8") as f:
        questions = list(csv.DictReader(f))

    hits = 0
    for item in questions:
        question, expected = item["question"], item["expected_guide"]
        matches = retrieve(question, guides)
        found = matches[0][0]["id"] if matches else "NONE"
        correct = found == expected
        hits += correct

        if matches:
            answer_v1 = ask_llm(build_messages("v1", question, matches), matches)
            answer_v2 = ask_llm(build_messages("v2", question, matches), matches)
        else:
            answer_v1 = answer_v2 = FALLBACK

        rows.append({
            "question": question, "expected_guide": expected, "found_guide": found,
            "retrieval_correct": "yes" if correct else "no",
            "answer_v1": answer_v1, "answer_v2": answer_v2,
            "v1_score": "", "v2_score": "",
        })
        print(f"{'OK ' if correct else 'MISS'} | {question} -> {found} (expected {expected})")

    RESULTS.parent.mkdir(exist_ok=True)
    with open(RESULTS, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nGuide matching: {hits}/{len(rows)} correct ({hits / len(rows):.0%})")
    print(f"Saved: {RESULTS}")


if __name__ == "__main__":
    main()
