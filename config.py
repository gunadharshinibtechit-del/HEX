"""
HEX CONFIGURATION
Change these settings to reuse the prototype for another decision-support domain.
- APP_TITLE / DOMAIN_LABEL: visible product naming
- FIELDS: input fields, labels, scoring weights, and descriptions (weights should total 1.0)
- RECOMMENDATION_THRESHOLD: score at/above this suggests "Recommend scholarship"; below suggests "Do not recommend yet"
- DECISION_OPTIONS: human review choices displayed in the review screen
Important: this is an illustrative weighted demo, not a validated eligibility model.
"""
APP_TITLE = "HEX"
DOMAIN_LABEL = "Merit Scholarship Review"
RECOMMENDATION_THRESHOLD = 70
FIELDS = [
    {"key": "academic", "label": "Academic performance", "short_label": "Academics", "weight": 0.45,
     "help": "Higher score means stronger academic performance.", "default": 75},
    {"key": "attendance", "label": "Attendance consistency", "short_label": "Attendance", "weight": 0.25,
     "help": "Higher score means more consistent attendance.", "default": 85},
    {"key": "need", "label": "Financial-need signal", "short_label": "Financial need", "weight": 0.30,
     "help": "Higher score means stronger demonstrated financial need.", "default": 70},
]
DECISION_OPTIONS = [
    {"value": "Agree — recommend scholarship", "title": "Agree — recommend scholarship",
     "description": "I agree with the AI-supported suggestion."},
    {"value": "Disagree — do not recommend", "title": "Disagree — do not recommend",
     "description": "My judgment differs; I do not support the suggestion."},
    {"value": "More information needed", "title": "More information needed",
     "description": "Pause the decision until evidence is verified."},
    {"value": "Human override", "title": "Human override",
     "description": "Record a different human decision and explain why."},
]
