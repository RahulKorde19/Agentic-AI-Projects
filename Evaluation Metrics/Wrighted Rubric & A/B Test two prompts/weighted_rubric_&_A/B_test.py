
import os

from dotenv import load_dotenv

from openai import OpenAI


load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Design a Weighted Rubric and A/B Test Two Prompts

# Problem Statement

# Your team is arguing about two versions of a system prompt. Opinions are not evidence. You need a custom, weighted rubric that reflects what your business actually cares about, and an A/B test that scores both prompt variants across several questions so you can declare a winner with numbers.

# Goal of the Problem

# Define a weighted rubric (correctness, coverage, coherence, conciseness), generate answers under two prompt variants, judge each answer, compute a weighted score, aggregate per variant, and declare the winner.

# Step-by-step solution

# Step 1 — Setup and the rubric weights

import json

import pandas as pd

from openai import OpenAI

# client = OpenAI(api_key=OPENAI_API_KEY)

 

WEIGHTS = {"correctness": 0.4, "coverage": 0.3,

         "coherence": 0.2, "conciseness": 0.1}

print("Weights sum to", sum(WEIGHTS.values()))

# Expected output

# Weights sum to 1.0

# Step 2 — The two prompt variants to compare

VARIANTS = {

  "A_plain":    "Answer the question.",

  "B_structured":"Answer in 2-3 sentences. Be accurate, cover all key parts, "

                  "and stay concise. No filler.",

}

questions = [

  "What are two risks of letting an AI agent act autonomously?",

  "In one or two sentences, what is data minimization?",

  "Give two ways to reduce hallucinations in a RAG agent.",

]

# Expected output

# (no output)

# Step 3 — Generate an answer for a given variant

def answer(system_prompt, question):

   resp = client.chat.completions.create(

      model="gpt-4o-mini",

      messages=[{"role": "system", "content": system_prompt},

                {"role": "user", "content": question}],

      temperature=0,

   )

   return resp.choices[0].message.content

# Expected output

# (no output)

# Step 4 — Judge an answer on all four rubric axes (1-5)

def judge(question, ans):

   prompt = f"""Score the ANSWER from 1-5 on each axis.

Reply ONLY as JSON with keys correctness, coverage, coherence, conciseness.

QUESTION: {question}

ANSWER: {ans}"""

   resp = client.chat.completions.create(

      model="gpt-4o-mini",

      messages=[{"role": "user", "content": prompt}],

      temperature=0,

      response_format={"type": "json_object"},

   )

   return json.loads(resp.choices[0].message.content)

# Expected output

# (no output)

# Step 5 — Weighted score helper

def weighted(scores):

   return sum(scores[k] * w for k, w in WEIGHTS.items())

# Expected output

# (no output)

# Step 6 — Run the A/B evaluation

rows = []

for name, sys_prompt in VARIANTS.items():

   for q in questions:

       a = answer(sys_prompt, q)

       s = judge(q, a)

       rows.append({"variant": name, "score": round(weighted(s), 2)})

   print("done variant:", name)

 

df = pd.DataFrame(rows)

# Expected output

# done variant: A_plain

# done variant: B_structured

# Step 7 — Aggregate and declare the winner

summary = df.groupby("variant")["score"].mean().round(2)

print(summary.to_string())

winner = summary.idxmax()

print("\nWINNER:", winner, "with", summary.max(), "/ 5")

# Expected output

# variant

# A_plain        3.85

# B_structured   4.55

 

# WINNER: B_structured with 4.55 / 5

 

# (Exact numbers vary; the structured prompt usually wins.)

 