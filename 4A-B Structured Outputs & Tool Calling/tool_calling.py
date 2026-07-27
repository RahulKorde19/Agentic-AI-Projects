import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))




# Problem Statement: Your complaints pipeline should turn any free-text customer message into a validated record it can write straight into a database. You will do this the way agents do it — by having the model call a tool with strictly-typed arguments — and validate the result with Pydantic before trusting it.

# Goal of the Problem: Define a tool schema, force the model to call it, parse the arguments, and validate them into a typed object. This is your Module 1.2 deliverable.

# Where to run: VS Code (recommended)   ·  Est. time: 30 min   ·   Concepts: tool/function calling, schema validation, robustness

# Step 1 — Define the tool the model may call

tools = [{

   "type": "function",

   "function": {

       "name": "record_complaint",

       "description": "Record a structured customer complaint into the CRM.",

       "strict": True,

       "parameters": {

           "type": "object",

           "properties": {

               "customer_name": {"type": "string"},

               "product":       {"type": "string"},

               "issue_summary": {"type": "string"},

               "sentiment":     {"type": "string", "enum": ["angry", "neutral", "satisfied"]},

               "priority":      {"type": "integer", "description": "1 (low) to 5 (urgent)"},

           },

           "required": ["customer_name", "product", "issue_summary", "sentiment", "priority"],

           "additionalProperties": False,

      },

   },

}]

# Expected output

# # defines the tools list; no output

# Step 2 — Define a Pydantic model to validate what comes back

from pydantic import BaseModel, field_validator

from typing import Literal

 

class Complaint(BaseModel):

   customer_name: str

   product: str

   issue_summary: str

   sentiment: Literal["angry", "neutral", "satisfied"]

   priority: int

 

   @field_validator("priority")

   @classmethod

   def in_range(cls, v):

       if not 1 <= v <= 5:

           raise ValueError("priority must be 1..5")

       return v

# Expected output

# # defines the Complaint model; no output

# Step 3 — Force the tool call and parse the arguments

import json

 

def extract(message: str) -> Complaint:

   r = client.chat.completions.create(

       model="gpt-4.1-mini",

       messages=[

           {"role": "system", "content": "Call record_complaint with fields taken only from the message."},

           {"role": "user",   "content": message},

       ],

       tools=tools,

       tool_choice={"type": "function", "function": {"name": "record_complaint"}},

       temperature=0,

   )

   call = r.choices[0].message.tool_calls[0]

   args = json.loads(call.function.arguments)   # strict schema -> valid JSON

   return Complaint(**args)                      # Pydantic validates types & range

 

result = extract("I'm furious — my home loan EMI was debited twice this month! - Meera")

print(result.model_dump())

# Expected output

# {'customer_name': 'Meera', 'product': 'home loan', 'issue_summary': 'EMI debited twice in one month', 'sentiment': 'angry', 'priority': 5}

# Step 4 — Confirm validation actually protects you

# Prove the guard works by feeding a bad record straight to the model (bypassing the LLM):

from pydantic import ValidationError

 

try:

   Complaint(customer_name="Test", product="card", issue_summary="x",

             sentiment="angry", priority=9)   # 9 is out of range

except ValidationError as e:

   print("Rejected as expected:")

   print(e.errors()[0]["msg"])

# Expected output

# Rejected as expected:

# Value error, priority must be 1..5

# Note:  Two layers of safety: strict tool schema makes the model produce well-shaped JSON, and Pydantic re-checks types and business rules before anything reaches your database. Both matter.