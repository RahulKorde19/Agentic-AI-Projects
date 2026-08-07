import os

from dotenv import load_dotenv

from openai import OpenAI


load_dotenv()                     # reads .env into environment variables

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Add Logging & a Trace to an LLM Call

# Problem Statement

# When an LLM call misbehaves you usually have nothing to look at - no input, no output, no timing, no error. You are debugging blind. You need a lightweight way to record what went in, what came out, how long it took, and how many tokens it used.

# Goal of the Problem

# Wrap an LLM call with a tracing decorator that logs the inputs, output preview, latency, token usage and any errors into a trace list you can inspect.

# Step-by-step solution

# Step 1 — Set up logging and a trace store

import logging, time, json, functools

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

 

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")

logger = logging.getLogger("agent")

trace = []  # every traced call appends a record here

# Expected output

# (no output)

# Step 2 — Write a @traced decorator

def traced(func):

   @functools.wraps(func)

   def wrapper(*args, **kwargs):

      record = {"step": func.__name__, "input": str(args) + str(kwargs)}

      start = time.time()

      try:

          result = func(*args, **kwargs)

          record["status"] = "ok"

          record["output_preview"] = str(result)[:80]

          return result

      except Exception as e:

          record["status"] = "error"

          record["error"] = str(e)

          logger.error("%s FAILED: %s", func.__name__, e)

          raise

      finally:

          record["latency_s"] = round(time.time() - start, 2)

          trace.append(record)

          logger.info("%s | %ss | %s",

                      record["step"], record["latency_s"], record["status"])

   return wrapper

# Expected output

# (no output)

# Step 3 — Wrap a real LLM call and capture token usage

@traced

def summarize(text):

   resp = client.chat.completions.create(

      model="gpt-4o-mini",

      messages=[{"role": "user", "content": "Summarize in one line: " + text}],

      temperature=0,

   )
   trace_tokens.append(resp.usage.total_tokens)

   return resp.choices[0].message.content

 

trace_tokens = []

out = summarize("Agent evaluation is hard because outputs are open-ended and non-deterministic.")

print("SUMMARY:", out)

print("TOKENS :", trace_tokens[-1])

# Expected output

# INFO | summarize | 0.79s | ok

# SUMMARY: Agent evaluation is difficult due to open-ended, non-deterministic outputs.

# TOKENS : 41

 

# (Wording and exact numbers will vary.)

# Step 4 — Inspect the trace

print(json.dumps(trace, indent=2))

# Expected output

# [

#  {

#   "step": "summarize",

#    "input": "('Agent evaluation is hard...',){}",

#   "status": "ok",

#   "output_preview": "Agent evaluation is difficult due to...",

#   "latency_s": 0.79

#  }

# ]

 

 

 