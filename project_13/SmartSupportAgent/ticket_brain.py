import json
import re

from settings import (
    GEMINI_API_KEY,
    DEFAULT_MODEL,
    DEPARTMENTS,
    PRIORITIES,
    SENTIMENTS,
    SLA_HOURS
)

try:
    from google import genai
except ImportError:
    genai = None


# ============================================================
# SMART KEYWORD FALLBACK
# ============================================================

def smart_fallback(email):

    text = email.lower()

    security_keywords = [
        "unauthorized",
        "hacked",
        "hack",
        "fraud",
        "stolen",
        "suspicious",
        "2fa",
        "two-factor",
        "authentication",
        "someone accessed",
        "account accessed",
        "security"
    ]

    billing_keywords = [
        "charge",
        "charged",
        "refund",
        "payment",
        "credit card",
        "debit card",
        "invoice",
        "billing",
        "transaction",
        "money"
    ]

    technical_keywords = [
        "error",
        "bug",
        "api",
        "server",
        "500",
        "404",
        "webhook",
        "crash",
        "broken",
        "not working",
        "production",
        "checkout",
        "application"
    ]

    critical_keywords = [
        "unauthorized",
        "hacked",
        "fraud",
        "stolen",
        "someone accessed",
        "security breach",
        "completely broken",
        "every request",
        "immediately"
    ]

    high_keywords = [
        "production",
        "urgent",
        "broken",
        "not working",
        "error",
        "immediately"
    ]

    angry_keywords = [
        "angry",
        "ridiculous",
        "terrible",
        "unacceptable",
        "refund my money",
        "before i contact",
        "immediately"
    ]

    frustrated_keywords = [
        "frustrated",
        "problem",
        "issue",
        "broken",
        "error",
        "unable",
        "can't",
        "cannot"
    ]

    # --------------------------------------------------------
    # DEPARTMENT
    # --------------------------------------------------------

    if any(word in text for word in security_keywords):
        department = "Security & Fraud"

    elif any(word in text for word in billing_keywords):
        department = "Billing & Finance"

    elif any(word in text for word in technical_keywords):
        department = "Technical Support"

    else:
        department = "General Inquiry"

    # --------------------------------------------------------
    # PRIORITY
    # --------------------------------------------------------

    if any(word in text for word in critical_keywords):
        priority = "Critical"

    elif any(word in text for word in high_keywords):
        priority = "High"

    elif department == "General Inquiry":
        priority = "Low"

    else:
        priority = "Medium"

    # --------------------------------------------------------
    # SENTIMENT
    # --------------------------------------------------------

    if any(word in text for word in angry_keywords):
        sentiment = "Angry"

    elif any(word in text for word in frustrated_keywords):
        sentiment = "Frustrated"

    elif any(
        word in text
        for word in ["thanks", "thank you", "great", "love"]
    ):
        sentiment = "Pleased"

    else:
        sentiment = "Neutral"

    sla = SLA_HOURS[priority]

    reasoning = (
        f"The ticket was routed to {department} based on "
        f"the customer's primary issue. {priority} priority "
        f"was assigned according to urgency and potential impact."
    )

    return {
        "department": department,
        "priority": priority,
        "sentiment": sentiment,
        "sla_response_hours": sla,
        "reasoning": reasoning
    }


# ============================================================
# CLEAN GEMINI JSON
# ============================================================

def clean_json(text):

    text = text.strip()

    text = re.sub(
        r"```json",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"```",
        "",
        text
    )

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        text = text[start:end + 1]

    return json.loads(text)


# ============================================================
# GEMINI TICKET ANALYZER
# ============================================================

def analyze_ticket(email):

    if not email or not email.strip():

        return {
            "department": "General Inquiry",
            "priority": "Low",
            "sentiment": "Neutral",
            "sla_response_hours": 48,
            "reasoning": "No customer inquiry was provided."
        }

    if (
        genai is None
        or not GEMINI_API_KEY
        or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY"
    ):
        return smart_fallback(email)

    try:

        client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        prompt = f"""
You are an intelligent enterprise customer-support
triage engine.

Analyze the customer inquiry below.

Return ONLY valid JSON.

STRICT JSON SCHEMA:

{{
    "department":
        "Billing & Finance"
        | "Technical Support"
        | "Security & Fraud"
        | "General Inquiry",

    "priority":
        "Critical"
        | "High"
        | "Medium"
        | "Low",

    "sentiment":
        "Angry"
        | "Frustrated"
        | "Neutral"
        | "Pleased",

    "sla_response_hours":
        2 | 6 | 24 | 48,

    "reasoning":
        "Short justification of the department and urgency."
}}

SLA RULES:

Critical = 2 hours
High = 6 hours
Medium = 24 hours
Low = 48 hours

ROUTING RULES:

Billing/payment/refund/invoice issues
-> Billing & Finance

API/application/technical/error issues
-> Technical Support

Fraud/unauthorized access/security/authentication
-> Security & Fraud

Other questions
-> General Inquiry

CUSTOMER INQUIRY:

{email}
"""

        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )

        result = clean_json(response.text)

        if result["department"] not in DEPARTMENTS:
            raise ValueError("Invalid department")

        if result["priority"] not in PRIORITIES:
            raise ValueError("Invalid priority")

        if result["sentiment"] not in SENTIMENTS:
            raise ValueError("Invalid sentiment")

        result["sla_response_hours"] = (
            SLA_HOURS[result["priority"]]
        )

        return result

    except Exception:
        return smart_fallback(email)


# ============================================================
# RISK CALCULATOR
# ============================================================

def calculate_risk(ticket):

    priority_score = {
        "Critical": 60,
        "High": 40,
        "Medium": 20,
        "Low": 5
    }

    sentiment_score = {
        "Angry": 25,
        "Frustrated": 15,
        "Neutral": 5,
        "Pleased": 0
    }

    score = (
        priority_score.get(
            ticket["priority"],
            0
        )
        +
        sentiment_score.get(
            ticket["sentiment"],
            0
        )
    )

    if ticket["department"] == "Security & Fraud":
        score += 15

    return min(score, 100)


# ============================================================
# RISK LABEL
# ============================================================

def get_risk_label(score):

    if score >= 80:
        return "EXTREME"

    if score >= 60:
        return "HIGH RISK"

    if score >= 35:
        return "MODERATE"

    return "LOW RISK"