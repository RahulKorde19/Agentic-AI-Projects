
# Exercise 5B  Self-Improving Plan (Generate → Evaluate → Improve)    DEEP DIVE

 

# Problem Statement:  A Planner drafts a plan; a Critic scores it 1–10 and gives feedback; the Planner revises. Loop until the score reaches 8 or you hit the iteration limit.

# Goal of the Problem:  Implement a reinforcement-style planning loop where an evaluator acts as the reward signal.

 

# Step 1 —  Install the library and set your API key

# Run this once per session. Paste the OpenAI API key you were given.

# Python

# pip install openai --quiet

 

# Python

import os

os.environ["OPENAI_API_KEY"] = "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"


 

# Expected output

# (No output. The key is now available to the OpenAI client.)

 

# Step 2 —  Define the Planner and the Critic (reward signal)

# Python

from openai import OpenAI

import json

client = OpenAI()

 

def plan_step(goal, feedback=None):

  user = f"Goal: {goal}"

  if feedback:

       user += f"\nImprove the plan using this feedback: {feedback}"

  r = client.chat.completions.create(model="gpt-4o-mini",

       messages=[{"role": "system", "content": "Produce a concise 4-step plan."},

                 {"role": "user", "content": user}])

  return r.choices[0].message.content

 

def critic(goal, plan):

  r = client.chat.completions.create(model="gpt-4o-mini",

       response_format={"type": "json_object"},

       messages=[{"role": "system", "content":

                    'Score the plan 1-10 for feasibility and completeness. '

                    'Return JSON {"score": int, "feedback": "one improvement"}'},

                 {"role": "user", "content": f"Goal: {goal}\nPlan: {plan}"}])

  return json.loads(r.choices[0].message.content)

 

# Expected output

# (No output - a Planner and a Critic. The Critic is the "reward signal".)

 

# Step 3 —  Run the improvement loop

# Python

goal = "Reduce our monthly cloud bill by 30% within one quarter"

plan = plan_step(goal)

 

for i in range(1, 4):                       # up to 3 improvement iterations

  review = critic(goal, plan)

  print(f"Iteration {i}: score={review['score']} | {review['feedback'][:70]}")

  if review["score"] >= 8:

       print("Goal met - stopping."); break

  plan = plan_step(goal, review["feedback"])   # revise using feedback

 

print("\n===== FINAL PLAN =====\n")

print(plan)

 

# Expected output

# Iteration 1: score=6 | Add specific cost-monitoring and set measurable targets

# Iteration 2: score=8 | Looks feasible and measurable

# Goal met - stopping.

 

# ===== FINAL PLAN =====
