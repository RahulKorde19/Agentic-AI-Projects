# /simplest): paste your key directly. Option B (recommended in Colab): store it in Secrets, then read it.

# Option A - quick, but do not share this cell


OPENAI_API_KEY="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"
# Option B - Colab Secrets (safer)

# from google.colab import userdata

# OPENAI_API_KEY = userdata.get("OPENAI_API_KEY")

 

from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

print("OpenAI client ready:", client is not None)

# Expected output

# OpenAI client ready: True

 

# (Coding Track)

# Task Success Rate & Latency

# Problem Statement

# You built a simple question-answering assistant. Before you trust it, you need numbers: how often does it get the right answer, and how fast? Right now you have no idea, and 'it feels okay' is not an evaluation.

# Goal of the Problem

# Run the assistant over a small labelled test set and compute two metrics: task success rate (% of answers that contain the correct key fact) and average latency in seconds.

# Step-by-step solution

# Step 1 — Import what you need

import time

from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

# Expected output

# (no output - the cell just runs)

# Step 2 — Define a small labelled test set

# Each case has a question and the key fact the correct answer must contain.

test_cases = [

  {"question": "What is the capital of France?",        "expected": "Paris"},

  {"question": "What is 12 multiplied by 8?",           "expected": "96"},

  {"question": "Who wrote the play Romeo and Juliet?",  "expected": "Shakespeare"},

  {"question": "What is the chemical symbol for gold?", "expected": "Au"},

  {"question": "On which continent is Egypt located?",  "expected": "Africa"},

]

print("Loaded", len(test_cases), "test cases")

# Expected output

# Loaded 5 test cases

# Step 3 — Write an ask() function that also times the call

def ask(question):

   start = time.time()

   resp = client.chat.completions.create(

      model="gpt-4o-mini",

      messages=[{"role": "user", "content": question}],

      temperature=0,

   )

   latency = time.time() - start

   return resp.choices[0].message.content, latency

# Expected output

# (no output - function defined)

# Step 4 — Run every test case and score it

results = []

for case in test_cases:

  answer, latency = ask(case["question"])

  success = case["expected"].lower() in answer.lower()

  results.append({"success": success, "latency": latency})

  print("PASS" if success else "FAIL", "|",

        round(latency, 2), "s |", case["question"])

# Expected output

# PASS | 0.71 s | What is the capital of France?

# PASS | 0.68 s | What is 12 multiplied by 8?

# PASS | 0.83 s | Who wrote the play Romeo and Juliet?

# PASS | 0.66 s | What is the chemical symbol for gold?

# PASS | 0.74 s | On which continent is Egypt located?

 

# (Exact seconds will vary. You should see PASS on all or most rows.)

# Step 5 — Compute the two headline metrics

total = len(results)

passed = sum(r["success"] for r in results)

avg_latency = sum(r["latency"] for r in results) / total

 

print(f"Task success rate: {passed}/{total} = {passed/total:.0%}")

print(f"Average latency:   {avg_latency:.2f} s")

# Expected output

# Task success rate: 5/5 = 100%

# Average latency:   0.72 s

# Try changing temperature to 1.0 in Step 3 and re-running. Watch whether success rate drops - that is evaluation catching a regression before your users do.

 