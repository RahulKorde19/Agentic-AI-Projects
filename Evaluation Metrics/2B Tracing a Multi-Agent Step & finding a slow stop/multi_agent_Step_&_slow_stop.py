 

 
import os

from dotenv import load_dotenv

from openai import OpenAI


load_dotenv()                     # reads .env into environment variables

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

 

# Trace a Multi-Step Agent and Find the Slow Step

# Problem Statement

# Your agent plans, calls a tool, then writes a final answer. When it is slow or wrong, you cannot tell which of the three steps is to blame. You need per-step tracing (spans) so you can point at the exact stage that failed or dragged.

# Goal of the Problem

# Build a 3-step agent (plan -> tool -> synthesize), record a span for each step with its latency and status, then analyse the trace to identify the slowest step and confirm the tool ran correctly.

# Step-by-step solution

# Step 1 — Setup and a shared trace

import time, json

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

 

spans = []

def span(name, status, latency, detail=""):

  spans.append({"step": name, "status": status,

                "latency_s": round(latency, 2), "detail": detail[:60]})

# Expected output

# (no output)

# Step 2 — A simple tool the agent can call

def calculator(expression):

   # only allow digits and basic math operators

   allowed = set("0123456789+-*/.() ")

   if not set(expression) <= allowed:

      raise ValueError("unsafe expression")

   return eval(expression)

# Expected output

# (no output)

# Step 3 — Step 1 of the agent: PLAN (ask the model for the math expression)

def plan(question):

   start = time.time()

   resp = client.chat.completions.create(

      model="gpt-4o-mini",

      messages=[{"role": "user", "content":

          "Convert this into a single arithmetic expression, digits and "

          "operators only, no words:\n" + question}],

      temperature=0,

   )

   expr = resp.choices[0].message.content.strip()

   span("plan", "ok", time.time() - start, expr)

   return expr

# Expected output

# (no output)

# Step 4 — Step 2: run the TOOL (traced separately)

def run_tool(expr):

   start = time.time()

   try:

      result = calculator(expr)

      span("tool", "ok", time.time() - start, f"{expr} = {result}")

      return result

   except Exception as e:

      span("tool", "error", time.time() - start, str(e))

      raise

# Expected output

# (no output)

# Step 5 — Step 3: SYNTHESIZE a friendly answer

def synthesize(question, result):

   start = time.time()

   resp = client.chat.completions.create(

      model="gpt-4o-mini",

      messages=[{"role": "user", "content":

          f"Question: {question}\nComputed result: {result}\n"

          "Write a one-sentence friendly answer."}],

      temperature=0,

   )

   answer = resp.choices[0].message.content

   span("synthesize", "ok", time.time() - start, answer)

   return answer

# Expected output

# (no output)

# Step 6 — Orchestrate the full agent

def agent(question):

   expr = plan(question)

   result = run_tool(expr)

   return synthesize(question, result)

 

final = agent("If I buy 3 items at 19.99 each and add 8% tax, what is the total?")

print("FINAL:", final)

# Expected output

# FINAL: Your total for 3 items at 19.99 each plus 8% tax is 64.77.

 

# (Wording will vary; the number should be ~64.77.)

# Step 7 — Analyse the trace: which step was slowest?

print(json.dumps(spans, indent=2))

slowest = max(spans, key=lambda s: s["latency_s"])

print("\nSlowest step:", slowest["step"], "at", slowest["latency_s"], "s")

print("All steps ok?  ", all(s["status"] == "ok" for s in spans))

# Expected output

# [

# {"step": "plan", "status": "ok", "latency_s": 0.71, "detail": "3 * 19.99 * 1.08"},

# {"step": "tool", "status": "ok", "latency_s": 0.0, "detail": "3 * 19.99 * 1.08 = 64.77"},

# {"step": "synthesize", "status": "ok", "latency_s": 0.84, "detail": "Your total ..."}

# ]

 

# Slowest step: synthesize at 0.84 s

# All steps ok?   True