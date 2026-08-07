import os

from dotenv import load_dotenv

from openai import OpenAI


load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



# A Multi-Metric Evaluation Harness with a Report

# Problem Statement

# Your team's assistant answers customer questions that need several facts, not just one. A single pass/fail is too crude. You need a harness that scores correctness (is it right?), coverage (did it mention all the required points?) and latency, across a dataset, and produces a report you can share and re-run every time the prompt changes.

# Goal of the Problem

# Build a reusable evaluation harness. For each item, generate an answer, judge correctness with an LLM-as-a-judge, compute coverage against required key points, record latency, then output a pandas table plus a summary and save it to CSV.

# Step-by-step solution

# Step 1 — Imports and client

import time, json

import pandas as pd

from openai import OpenAI

# client = OpenAI(api_key=OPENAI_API_KEY)

# Expected output

# (no output)

# Step 2 — Build an evaluation dataset with required key points

dataset = [

   {

      "question": "What are three benefits of the Python list comprehension?",

      "key_points": ["concise", "readable", "faster"],

   },

   {

      "question": "Name two risks of hardcoding an API key in your code.",

      "key_points": ["leak", "commit"],

   },

   {

      "question": "What does a RAG system do in two steps?",

      "key_points": ["retrieve", "generate"],

   },

]

print("Dataset size:", len(dataset))

# Expected output

# Dataset size: 3

# Step 3 — The agent under test

def agent_answer(question):

   start = time.time()

   resp = client.chat.completions.create(

      model="gpt-4o-mini",

      messages=[

          {"role": "system", "content": "Answer clearly in 2-3 sentences."},

          {"role": "user", "content": question},

       ],

      temperature=0,

   )

   return resp.choices[0].message.content, time.time() - start

# Expected output

# (no output)

# Step 4 — An LLM-as-a-judge for correctness (returns strict JSON)

def judge_correctness(question, answer):

   prompt = (

      "You are a strict grader. Given a QUESTION and an ANSWER, "

      "decide if the answer is factually correct and on-topic. "

      "Reply ONLY with JSON: {\"correct\": 1} or {\"correct\": 0}.\n\n"

      f"QUESTION: {question}\nANSWER: {answer}"

   )

   resp = client.chat.completions.create(

      model="gpt-4o-mini",

      messages=[{"role": "user", "content": prompt}],

      temperature=0,

      response_format={"type": "json_object"},

   )

   return int(json.loads(resp.choices[0].message.content)["correct"])

# Expected output

# (no output)  

# Step 5 — A coverage metric (fraction of key points present)

def coverage(answer, key_points):

   hits = sum(1 for kp in key_points if kp.lower() in answer.lower())

   return hits / len(key_points)

# Expected output

# (no output)

# Step 6 — Run the harness over the whole dataset

rows = []

for item in dataset:

  answer, latency = agent_answer(item["question"])

  rows.append({

      "question": item["question"][:40] + "...",

      "correct": judge_correctness(item["question"], answer),

      "coverage": round(coverage(answer, item["key_points"]), 2),

      "latency_s": round(latency, 2),

   })

  print("scored:", item["question"][:40])

# Expected output

# scored: What are three benefits of the Python li

# scored: Name two risks of hardcoding an API key i

# scored: What does a RAG system do in two steps?

# Step 7 — Build the report, print a summary, save CSV

df = pd.DataFrame(rows)

print(df.to_string(index=False))

print()

print("Correctness rate :", f"{df['correct'].mean():.0%}")

print("Avg coverage     :", f"{df['coverage'].mean():.0%}")

print("Avg latency      :", f"{df['latency_s'].mean():.2f} s")

df.to_csv("eval_report.csv", index=False)

print("Saved eval_report.csv")

# Expected output

#                                  question  correct coverage  latency_s

# What are three benefits of the Python li...       1      1.00       1.12

# Name two risks of hardcoding an API key i...      1      1.00       0.95

#      What does a RAG system do in two steps?        1      1.00      0.88

 

# Correctness rate : 100%

# Avg coverage    : 100%

# Avg latency     : 0.98 s

# Saved eval_report.csv