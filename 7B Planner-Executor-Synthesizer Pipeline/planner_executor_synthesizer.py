
# Exercise 4B  Planner → Executor → Synthesizer Pipeline    DEEP DIVE

# Environment: Google Colab (Python + OpenAI)     Est. time: 20 min

# Problem Statement:  A Planner decomposes a goal into subtasks, an Executor completes each subtask in order (passing results forward), and a Synthesizer assembles the final deliverable.

# Goal of the Problem:  Implement hierarchical planning and watch intermediate state flow from one subtask to the next.

 

# Step 1 —  Install the library and set your API key

# Run this once per session. Paste the OpenAI API key you were given.

# Python

# !pip install openai --quiet

 

# Python

import os

os.environ["OPENAI_API_KEY"] = "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"

 

# Expected output

# (No output. The key is now available to the OpenAI client.)

 

# Step 2 —  Define the Planner

# Python

from openai import OpenAI

import json

client = OpenAI()

 

def planner(goal):

  r = client.chat.completions.create(

       model="gpt-4o-mini", response_format={"type": "json_object"},

       messages=[

         {"role": "system", "content":

           'Return JSON {"tasks":[{"id":1,"task":...}]}. 3-5 ordered subtasks.'},

        {"role": "user", "content": f"Goal: {goal}"}])

  return json.loads(r.choices[0].message.content)

 

# Expected output

# (No output - the Planner that decomposes the goal.)

 

# Step 3 —  Define the Executor

# Python

def executor(task, context):

  r = client.chat.completions.create(

       model="gpt-4o-mini",

       messages=[

         {"role": "system", "content": "You complete ONE subtask. Be concise. Use any prior results provided."},

         {"role": "user", "content": f"Subtask: {task}\n\nPrior results:\n{context}"}])

  return r.choices[0].message.content

 

# Expected output

# (No output - the Executor that completes one subtask at a time.)

 

# Step 4 —  Run the plan → execute loop

# Python

goal = "Create a one-page competitor comparison of two note-taking apps"

plan = planner(goal)

results = []

for t in plan["tasks"]:

  context = "\n".join(results) if results else "(none yet)"

  output = executor(t["task"], context)

  print(f"\n--- Task {t['id']}: {t['task']} ---")

  print(output)

  results.append(f"Task {t['id']} result: {output}")

 

# Expected output

# --- Task 1: Identify two note-taking apps to compare ---

# Notion and Evernote ...

# --- Task 2: List comparison criteria ---

# Pricing, offline mode, collaboration ...

# --- Task 3: Compare the apps on each criterion ---

# ...

# # Each task's result is passed forward as context to the next (hierarchical flow).

 

# Step 5 —  Synthesize the final deliverable

# Python

final = client.chat.completions.create(

  model="gpt-4o-mini",

  messages=[{"role": "system", "content": "Combine the results into a clean one-page comparison."},

             {"role": "user", "content": "\n".join(results)}]

).choices[0].message.content

print("\n===== FINAL DELIVERABLE =====\n")

print(final)

 

# Expected output

# ===== FINAL DELIVERABLE =====

 

# Note-Taking Apps: Notion vs Evernote

# | Criterion | Notion | Evernote | ...

# (a tidy one-page comparison assembled from all sub-results)

 