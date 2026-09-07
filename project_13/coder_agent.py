# coder_agent.py

import re
import google.generativeai as genai

from config import API_KEY, DEFAULT_MODEL


# Configure Gemini
genai.configure(api_key=API_KEY)


def clean_code(text):
    """
    Removes Markdown code fences from Gemini's response.
    """

    text = text.strip()

    # Remove ```python ... ```
    text = re.sub(r"^```python\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    return text.strip()


def generate_code(prompt):
    """
    Ask Gemini to generate the initial Python function.
    """

    model = genai.GenerativeModel(DEFAULT_MODEL)

    instruction = f"""
You are an expert Python programmer.

Write ONLY the Python function requested below.

Do not explain the answer.
Do not use Markdown.
Do not include ```python or ```.

Problem:
{prompt}
"""

    response = model.generate_content(instruction)

    return clean_code(response.text)


def repair_code(prompt, old_code, error):
    """
    Ask Gemini to repair the failed Python function.
    """

    model = genai.GenerativeModel(DEFAULT_MODEL)

    instruction = f"""
You are an expert Python debugging agent.

The following Python function was generated for this problem:

PROBLEM:
{prompt}

CURRENT CODE:
{old_code}

The code failed the hidden tests.

ERROR / TRACEBACK:
{error}

Repair the function so that it correctly handles all edge cases.

Return ONLY the complete corrected Python function.

Do not explain anything.
Do not use Markdown.
Do not include ```python or ```.
"""

    response = model.generate_content(instruction)

    return clean_code(response.text)