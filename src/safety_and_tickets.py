"""Two small helpers: hide personal data and write tickets to a CSV file."""
import csv
import re
from datetime import datetime
from pathlib import Path

TICKETS_FILE = Path(__file__).resolve().parent.parent / "data" / "tickets.csv"

# Patterns for data we do not want to send to an AI service.
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
LONG_NUMBER = re.compile(r"\b\d[\d\s/-]{7,}\d\b")  # phone numbers, card numbers, ...
IBAN = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{10,30}\b")


def redact(text):
    """Replace emails, long numbers and IBANs before the text leaves the computer."""
    text = EMAIL.sub("[EMAIL]", text)
    text = IBAN.sub("[IBAN]", text)
    text = LONG_NUMBER.sub("[NUMBER]", text)
    return text


def log_ticket(question, status, guide_title=""):
    """Add one row to data/tickets.csv. Status: 'answered' or 'escalated'."""
    TICKETS_FILE.parent.mkdir(exist_ok=True)
    new_file = not TICKETS_FILE.exists()
    ticket_id = 1
    if not new_file:
        with open(TICKETS_FILE, encoding="utf-8") as f:
            ticket_id = sum(1 for _ in f)  # header line counts as 1, so next id = lines
    with open(TICKETS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["id", "time", "question", "status", "guide"])
        writer.writerow([ticket_id, datetime.now().isoformat(timespec="seconds"),
                         question, status, guide_title])
    return ticket_id
