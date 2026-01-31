"""
Author: Muthu Selvam
Email: muthucse7@gmail.com
"""

import os
from openai import OpenAI
import tiktoken
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env

MODEL = os.getenv("MODEL", "gpt-4.1-mini")
MAX_OUTPUT_TOKENS = int(os.getenv("MAX_OUTPUT_TOKENS", "350"))
PRICE_PER_1M_INPUT = float(os.getenv("PRICE_PER_1M_INPUT", "0.00"))
PRICE_PER_1M_OUTPUT = float(os.getenv("PRICE_PER_1M_OUTPUT", "0.00"))

BUSINESS_QUESTIONS = [
    "I forgot my online banking password. What are the steps to reset it securely?",
    "Why was my transfer marked as pending, and how long does it usually take to complete?",
    "How can I set up alerts for large transactions or low balance to avoid overdrafts?",
    "I see a charge I don’t recognize. What should I do and how do I dispute it?",
    "How do I add a new payee and what security checks are required?",
    "My card was declined, but I have funds. What are common reasons and how can I fix it?",
    "How can I schedule recurring transfers and confirm they were successfully set up?",
    "What’s the fastest way to contact support for a wire transfer issue?"
]

SYSTEM_STYLE = (
    "You are a U.S. bank customer support assistant. "
    "Give clear, step-by-step answers in plain language and avoid technical terms."
)

def estimate_cost(input_tokens: int, output_tokens: int) -> float:
    in_cost = (input_tokens / 1_000_000) * PRICE_PER_1M_INPUT
    out_cost = (output_tokens / 1_000_000) * PRICE_PER_1M_OUTPUT
    return in_cost + out_cost

def count_tokens(text: str, model: str = MODEL) -> int:
    try:
        enc = tiktoken.encoding_for_model(model)
    except Exception:
        enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set.")

    client = OpenAI(api_key=api_key)

    print(f"Using model: {MODEL}")
    print(f"Number of questions: {len(BUSINESS_QUESTIONS)}")
    print("-" * 60)

    total_in, total_out, total_est = 0, 0, 0.0

    for i, q in enumerate(BUSINESS_QUESTIONS, 1):
        resp = client.responses.create(
            model=MODEL,
            input=[
                {"role": "system", "content": SYSTEM_STYLE},
                {"role": "user", "content": q}
            ],
            max_output_tokens=MAX_OUTPUT_TOKENS
        )

        answer = ""
        try:
            answer = resp.output_text
        except Exception:
            answer = str(resp)

        in_tokens = None
        out_tokens = None
        try:
            usage = getattr(resp, "usage", None)
            if usage:
                in_tokens = getattr(usage, "input_tokens", None)
                out_tokens = getattr(usage, "output_tokens", None)
        except Exception:
            pass

        if in_tokens is None:
            in_tokens = count_tokens(SYSTEM_STYLE + "\n" + q)
        if out_tokens is None:
            out_tokens = count_tokens(answer)

        est = estimate_cost(in_tokens, out_tokens)

        total_in += in_tokens
        total_out += out_tokens
        total_est += est

        print(f"[{i}] Q: {q}")
        print(f"    Input tokens:  {in_tokens}")
        print(f"    Output tokens: {out_tokens}")
        print(f"    Estimated cost:     ${est:.6f}")
        print(f"    Answer: {answer[:400]}{'...' if len(answer) > 400 else ''}")
        print("-" * 60)

    print("TOTALS")
    print(f"  Total input tokens:  {total_in}")
    print(f"  Total output tokens: {total_out}")
    print(f"  Total estimated cost:     ${total_est:.6f}")
    print()
    print("To simulate scale (e.g., 10,000 or 1,000,000 calls), multiply the per-call cost.")
    print("Example: monthly_cost = avg_cost_per_call * 1000000")

if __name__ == "__main__":
    main()
