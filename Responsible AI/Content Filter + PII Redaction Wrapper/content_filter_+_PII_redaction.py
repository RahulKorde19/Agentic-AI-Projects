import os

from dotenv import load_dotenv

from openai import OpenAI


load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



# Content Filter + PII Redaction Wrapper

# Problem Statement

# Before user text reaches your agent (and before the agent's reply reaches the user) you need two guardrails: block clearly harmful input, and strip personal data like emails and phone numbers so it is never sent onward or logged in the clear.

# Goal of the Problem

# Write a wrapper that runs OpenAI moderation on incoming text, blocks it if flagged, and otherwise redacts emails and phone numbers before returning the safe text.

# Step-by-step solution

# Step 1 — Setup

import re

from openai import OpenAI

# client = OpenAI(api_key=OPENAI_API_KEY)

# Expected output

# (no output)

# Step 2 — A moderation check using OpenAI's moderation endpoint

def is_flagged(text):

   r = client.moderations.create(model="omni-moderation-latest", input=text)

   return r.results[0].flagged

 

print("harmless flagged?", is_flagged("How do I bake bread?"))

# Expected output

# harmless flagged? False

# Step 3 — A PII redactor (emails and phone numbers)

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")

PHONE = re.compile(r"\b(?:\+?\d{1,3}[- ]?)?\d{10}\b")

 

def redact(text):

   text = EMAIL.sub("[EMAIL]", text)

   text = PHONE.sub("[PHONE]", text)

   return text

 

print(redact("Contact me at asha@work.com or 9876543210 please."))

# Expected output

# Contact me at [EMAIL] or [PHONE] please.

# Step 4 — Combine into one guardrail wrapper

def safe_input(text):

   if is_flagged(text):

      return {"allowed": False, "text": None, "reason": "blocked by moderation"}

   return {"allowed": True, "text": redact(text), "reason": "ok"}

 

print(safe_input("My email is asha@work.com, help me plan a trip."))

# Expected output

# {'allowed': True, 'text': 'My email is [EMAIL], help me plan a trip.', 'reason': 'ok'}

# Redact BEFORE you send text to the model or write it to logs. Guardrails you apply after the data has left are too late.

 

 
