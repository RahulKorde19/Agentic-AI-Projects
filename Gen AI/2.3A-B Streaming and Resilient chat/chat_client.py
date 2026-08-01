import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Hands-On 3B · Stretch — A Resilient Chat Client

# Problem Statement: In production, calls occasionally time out or hit rate limits, and an unhandled error takes down a whole request. You need a small wrapper that retries sensibly, respects a timeout, and tracks token spend.

# Goal of the Problem:  Build a reusable ResilientChat class with exponential-backoff retries, a timeout, and running token/cost accounting.

# Where to run: VS Code (recommended)   

# Concepts: retries, timeouts, rate limits, cost control

# Step 1 — Import the specific error types

import time, random

from openai import OpenAI, RateLimitError, APITimeoutError, APIError

# Expected output

# # imports only; no output

# Step 2 — Build the client class

# The SDK has built-in retries, but writing them explicitly makes the strategy visible and tunable.

PRICES = {"gpt-4.1-mini": (0.40, 1.60)}  # per 1M tokens (in, out)

 

class ResilientChat:

   def __init__(self, model="gpt-4.1-mini", max_retries=4, timeout=20):

       self.client = OpenAI(timeout=timeout, max_retries=0)  # we do retries ourselves

       self.model = model

       self.max_retries = max_retries

       self.in_tok = 0

       self.out_tok = 0

 

   def complete(self, messages, **kwargs):

       for attempt in range(self.max_retries):

           try:

               r = self.client.chat.completions.create(

                   model=self.model, messages=messages, **kwargs

               )

               self.in_tok  += r.usage.prompt_tokens

               self.out_tok += r.usage.completion_tokens

               return r.choices[0].message.content

           except (RateLimitError, APITimeoutError, APIError) as e:

               wait = min(2 ** attempt + random.random(), 15)

               print(f"  [retry {attempt+1}/{self.max_retries}] {type(e).__name__} -> waiting {wait:.1f}s")

               time.sleep(wait)

       raise RuntimeError("Exhausted retries")

 

   def cost(self):
    pin, pout = PRICES[self.model]

    return (self.in_tok/1_000_000)*pin + (self.out_tok/1_000_000)*pout

# Expected output

# # defines the ResilientChat class; no output

# Step 3 — Use it for a few calls and read the running cost

bot = ResilientChat()

 

questions = [

   "What is a fixed deposit?",

   "How is FD interest taxed in India, in one line?",

   "Name one risk of breaking an FD early.",

]

for q in questions:

   answer = bot.complete(

       [{"role": "user", "content": q}],

       temperature=0, max_tokens=60,

   )

   print("Q:", q)

   print("A:", answer.strip(), "\n")

 

print(f"Total tokens: in={bot.in_tok}, out={bot.out_tok}")

print(f"Session cost: ${bot.cost():.6f}")

# Expected output

# Q: What is a fixed deposit?

# A: A fixed deposit is a savings product where you lock a sum for a set term at a fixed interest rate.

 

# Q: How is FD interest taxed in India, in one line?

# A: FD interest is added to your income and taxed at your applicable slab rate (TDS may apply).

 

# Q: Name one risk of breaking an FD early.

# A: Early withdrawal usually incurs a penalty and a lower interest rate.

 

# Total tokens: in=61, out=? (varies)

# Session cost: $0.0000xx

# Note:  If you never see a [retry ...] line, that's normal — retries only fire on transient errors. To watch the backoff work, you could temporarily lower the client timeout to a tiny value.

# Deliverable:  This class, saved as a small reusable module (e.g. resilient_chat.py), is the reliability layer every later RAG and agent exercise will build on.