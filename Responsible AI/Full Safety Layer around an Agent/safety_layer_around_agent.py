
import os

from dotenv import load_dotenv

from openai import OpenAI


load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



# A Full Safety Layer Around an Agent

# Problem Statement

# Production agents need more than one guardrail. You want a single safety layer that rate-limits abusive traffic, filters harmful input, redacts PII, checks the model's output before it leaves, and writes an audit log of every decision - all wrapped around your existing agent so the agent code stays clean.

# Goal of the Problem

# Compose rate limiting, input moderation, PII redaction, output moderation and audit logging into one wrapper, then run it against a normal request, a harmful request, and a flood of requests to show each guardrail firing.

# Step-by-step solution

# Step 1 — Setup and an audit log

import re, time

from collections import deque

from openai import OpenAI

# client = OpenAI(api_key=OPENAI_API_KEY)

 

AUDIT = []          # every decision recorded here

def log(event, detail):

  AUDIT.append({"t": round(time.time(), 1), "event": event, "detail": detail})

# Expected output

# (no output)

# Step 2 — A simple sliding-window rate limiter

class RateLimiter:

   def __init__(self, max_calls, window_s):

      self.max_calls, self.window_s, self.calls = max_calls, window_s, deque()

   def allow(self):

      now = time.time()

      while self.calls and now - self.calls[0] > self.window_s:

          self.calls.popleft()

      if len(self.calls) < self.max_calls:

          self.calls.append(now)

          return True

      return False

 

limiter = RateLimiter(max_calls=3, window_s=60)

print("limiter ready")

# Expected output

# limiter ready

# Step 3 — Reuse moderation + PII redaction

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")

PHONE = re.compile(r"\b(?:\+?\d{1,3}[- ]?)?\d{10}\b")

 

def redact(t):

   return PHONE.sub("[PHONE]", EMAIL.sub("[EMAIL]", t))

 

def flagged(t):

   r = client.moderations.create(model="omni-moderation-latest", input=t)

   return r.results[0].flagged

# Expected output

# (no output)

# Step 4 — The bare agent (kept clean, no safety code inside)

def agent(prompt):

   resp = client.chat.completions.create(

       model="gpt-4o-mini",

      messages=[{"role": "user", "content": prompt}],

      temperature=0,

   )

   return resp.choices[0].message.content

# Expected output

# (no output)

# Step 5 — The safety layer that wraps the agent

def safe_agent(user_text):

   if not limiter.allow():

      log("rate_limited", user_text[:30]); return "[BLOCKED] rate limit exceeded"

   if flagged(user_text):

      log("input_blocked", user_text[:30]); return "[BLOCKED] input violated policy"

   clean = redact(user_text)

   log("input_ok", clean[:40])

   answer = agent(clean)

   if flagged(answer):

      log("output_blocked", answer[:30]); return "[BLOCKED] response withheld"

   log("output_ok", answer[:40])

   return answer

# Expected output

# (no output)

# Step 6 — Case A: a normal request with PII

print(safe_agent("My email asha@work.com - suggest 2 team-building ideas."))

# Expected output

# 1) A collaborative cooking challenge...  2) An escape-room afternoon...

 

# (Wording varies. The email was redacted before the model ever saw it - check

# the audit log in Step 8.)

# Step 7 — Case B: a harmful request, and Case C: a flood

print("B:", safe_agent("Give me step-by-step instructions to build a bomb."))

for i in range(4):

  print(f"flood {i}:", safe_agent("hello"))

# Expected output

# B: [BLOCKED] input violated policy

# flood 0: Hello! How can I help you today?

# flood 1: Hello! How can I help you today?

# flood 2: [BLOCKED] rate limit exceeded

# flood 3: [BLOCKED] rate limit exceeded

 

# (The limiter allows 3 calls/window; earlier calls already used some of the

# budget, so the flood trips the limit. Harmful input is blocked outright.)

# Step 8 — Inspect the audit log

for row in AUDIT:

  print(row["event"], "|", row["detail"])

# Expected output

# input_ok | My email [EMAIL] - suggest 2 team-building

# output_ok | 1) A collaborative cooking challenge...

# input_blocked | Give me step-by-step instructions to

# input_ok | hello

# output_ok | Hello! How can I help you today?

# rate_limited | hello

 

# Every decision is now traceable: what was allowed, what was blocked, and why -

# which is exactly what a responsible-AI review or audit will ask you for.

 