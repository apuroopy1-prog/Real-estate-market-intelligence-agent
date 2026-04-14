"""guardrails/__init__.py — Input/output safety checks"""
import re

def check_input_length(text: str, max_chars: int = 10_000) -> str:
    if len(text) > max_chars:
        raise ValueError(f"Input too long: {len(text)} chars (max {max_chars})")
    return text

def sanitise_output(text: str) -> str:
    text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[SSN_REDACTED]", text)
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL_REDACTED]", text)
    return text
