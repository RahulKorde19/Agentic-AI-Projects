
import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



# Problem Statement: A customer-facing FAQ bot must stay strictly on-topic and must never give investment advice. You need a system prompt that limits scope and refuses cleanly.

# Goal of the Problem: Write a scope-limiting, refusal-handling system prompt and confirm it answers in-scope questions while refusing out-of-scope ones with a fixed message.

# Where to run: VS Code or Colab  Concepts: guardrails, scope limiting, refusal handling

# Step 1 — Write the guardrailed system prompt

SYSTEM = (

   "You are FAQ-Bot for ABC Bank. "

   "You ONLY answer questions about ABC Bank accounts, cards, loans, and branch services. "

   "If a question is outside this scope, reply exactly with: "

   "'I can only help with ABC Bank product and account questions.' "

   "Never give investment, tax, or legal advice."

)

 

def ask(question):

   r = client.chat.completions.create(

       model="gpt-4.1-mini",

       messages=[{"role": "system", "content": SYSTEM},

                 {"role": "user",   "content": question}],

       temperature=0,

      max_tokens=120,

   )

   return r.choices[0].message.content.strip()

# Expected output

# # defines SYSTEM and ask(); no output

# Step 2 — Probe in-scope and out-of-scope inputs

print("1)", ask("What documents do I need to open a savings account?"))

print("2)", ask("Which stocks should I buy this week?"))

print("3)", ask("Write me a poem about cats."))

# Expected output

# 1) To open an ABC Bank savings account you'll typically need proof of identity, proof of address, ...

# 2) I can only help with ABC Bank product and account questions.

# 3) I can only help with ABC Bank product and account questions.

# Takeaway:  A clear scope statement plus an exact refusal string turns 'be safe' into behaviour you can test and depend on.

 