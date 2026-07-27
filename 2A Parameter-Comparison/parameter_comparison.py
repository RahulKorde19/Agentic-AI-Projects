import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Problem Statement: Your team needs a repeatable way to decide default decoding settings for a feature, instead of arguing from anecdotes. Build a small harness that runs one prompt across several settings and records output, latency and token usage.

# Goal of the Problem: Produce an annotated comparison table across temperature / top_p / max_tokens, then prove reproducibility at temperature 0. This is your Module 1.1 deliverable.

# Where to run: VS Code or Colab   

# Concepts: temperature, top_p, max_tokens, latency, usage, reproducibility

# Step 1 — Define the prompt and the settings grid

import time

import pandas as pd

 

PROMPT = "Explain what an emergency fund is, in exactly two sentences."

 

CONFIGS = [

   {"temperature": 0.0, "top_p": 1.0, "max_tokens": 60},

   {"temperature": 0.7, "top_p": 1.0, "max_tokens": 60},

   {"temperature": 1.0, "top_p": 0.9, "max_tokens": 60},

   {"temperature": 0.0, "top_p": 1.0, "max_tokens": 20},   # truncation demo

]

# Expected output

# # defines PROMPT and CONFIGS; no printed output

# Step 2 — Run the grid and capture metrics

rows = []

for cfg in CONFIGS:

   t0 = time.time()

   r = client.chat.completions.create(

       model="gpt-4.1-mini",

       messages=[{"role": "user", "content": PROMPT}],

       **cfg,

   )

   latency = round(time.time() - t0, 2)

   rows.append({

       **cfg,

       "latency_s": latency,

       "prompt_tok": r.usage.prompt_tokens,

       "output_tok": r.usage.completion_tokens,

       "finish": r.choices[0].finish_reason,

       "output": r.choices[0].message.content.strip(),

   })

 

df = pd.DataFrame(rows)

print(df[["temperature","top_p","max_tokens","latency_s","output_tok","finish"]].to_string(index=False))

# Expected output

# temperature top_p  max_tokens  latency_s output_tok  finish

#         0.0   1.0          60       0.91          48   stop

#         0.7   1.0          60       0.88          52   stop

#         1.2   0.9          60       1.03          57   stop

#         0.0   1.0          20       0.42          20 length

 