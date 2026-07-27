
import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


#  Chain-of-Thought behind an Output Contract (Code Based) 

# Problem Statement: A loan pre-check needs the model to reason carefully, but the downstream system must receive a clean, fixed decision — never a paragraph. You want reasoning quality without leaking free text into your pipeline.

# Goal of the Problem: Let the model think step by step in a dedicated field while enforcing a strict output contract, so downstream code only ever reads a controlled decision.

# Where to run: VS Code or Colab  ·   Est. time: 25 min   ·  Concepts: chain-of-thought, output contracts, structured outputs

# Step 1 — Define the decision contract

schema = {

   "type": "object",

   "properties": {

       "reasoning":   {"type": "string", "description": "step-by-step working"},

       "decision":    {"type": "string", "enum": ["ELIGIBLE", "NOT_ELIGIBLE", "NEEDS_REVIEW"]},

       "key_factors": {"type": "array", "items": {"type": "string"}},

   },

   "required": ["reasoning", "decision", "key_factors"],

   "additionalProperties": False,

}

# Expected output

# # defines schema; no output

# Step 2 — Encode the business rules in the system prompt

RULES = (

   "Approve (ELIGIBLE) only if BOTH: total EMIs (existing + new) <= 50% of monthly income, "

   "AND credit score >= 700. "

   "If credit score is 650-699, return NEEDS_REVIEW. "

   "Otherwise return NOT_ELIGIBLE."

)

 

SYSTEM = (f"You are a loan pre-check assistant. Rules: {RULES} "

         "Work through the numbers in 'reasoning', then give the final 'decision'.")

# Expected output

# # defines RULES and SYSTEM; no output

# Step 3 — Run a case and read only the controlled fields

import json

 

applicant = ("Age 34, monthly income 90000, existing EMIs 55000, "

            "requested new loan EMI 20000, credit score 710.")

 

r = client.chat.completions.create(

   model="gpt-4.1-mini",

   messages=[{"role": "system", "content": SYSTEM},

             {"role": "user",   "content": applicant}],

   response_format={"type": "json_schema",

                    "json_schema": {"name": "verdict", "schema": schema, "strict": True}},

   temperature=0,

)

v = json.loads(r.choices[0].message.content)

 

print("DECISION   :", v["decision"])

print("KEY FACTORS:", v["key_factors"])

# downstream systems use v["decision"] only; reasoning is for audit/logs

# Expected output

# DECISION   : NOT_ELIGIBLE

# KEY FACTORS: ['Total EMIs 75000 exceed 50% of income (45000)', 'Credit score 710 is acceptable but EMI rule fails']

# Why NOT_ELIGIBLE: 50% of 90,000 income is 45,000, but total EMIs are 55,000 + 20,000 = 75,000 — over the limit, even though the credit score passes.

# Step 4 — Show the contract holds across cases

cases = [

   "Income 120000, existing EMIs 20000, new EMI 15000, credit score 760.", # ELIGIBLE

   "Income 80000, existing EMIs 10000, new EMI 10000, credit score 670.",  # NEEDS_REVIEW

]

for c in cases:

   r = client.chat.completions.create(

       model="gpt-4.1-mini",

       messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": c}],

       response_format={"type": "json_schema",

                       "json_schema": {"name": "verdict", "schema": schema, "strict": True}},

       temperature=0,

   )

   print(json.loads(r.choices[0].message.content)["decision"], "<-", c[:40], "...")

# Expected output

# ELIGIBLE <- Income 120000, existing EMIs 20000, new  ...

# NEEDS_REVIEW <- Income 80000, existing EMIs 10000, new E ...

# Takeaway:  Chain-of-thought improves accuracy on multi-step logic; putting it inside a schema field keeps the free-form reasoning out of your data path. Downstream code reads only decision.

 

