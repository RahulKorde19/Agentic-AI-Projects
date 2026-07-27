import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Hands-On 4A · Quick Win — JSON You Can Trust

# Problem Statement: A downstream system needs clean JSON, but free-text model output keeps breaking your parser. You want the model to return data that always matches a fixed shape.

# Goal of the Problem: Use Structured Outputs (json_schema, strict mode) to extract fields from a customer message into guaranteed-valid JSON.

# Where to run: VS Code or Colab  ·   Est. time: 15 min   ·  Concepts: JSON mode, response schemas

# Step 1 — Describe the shape you want

schema = {

   "type": "object",

   "properties": {

       "customer_name":  {"type": "string"},

       "account_type":   {"type": "string"},

       "issue_category": {"type": "string"},

       "urgency":        {"type": "string", "enum": ["low", "medium", "high"]},

   },

   "required": ["customer_name", "account_type", "issue_category", "urgency"],

   "additionalProperties": False,

}

# Expected output

# # defines schema; no output