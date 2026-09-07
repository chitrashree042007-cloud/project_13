import os

# ============================================================
# SMART SUPPORT AGENT - SETTINGS
# ============================================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    "")

DEFAULT_MODEL = "gemini-3.6-flash"

COMPANY_NAME = "ZIEERS Systems Pvt Ltd"

DEPARTMENTS = [
    "Billing & Finance",
    "Technical Support",
    "Security & Fraud",
    "General Inquiry"
]

PRIORITIES = [
    "Critical",
    "High",
    "Medium",
    "Low"
]

SENTIMENTS = [
    "Angry",
    "Frustrated",
    "Neutral",
    "Pleased"
]

SLA_HOURS = {
    "Critical": 2,
    "High": 6,
    "Medium": 24,
    "Low": 48
}