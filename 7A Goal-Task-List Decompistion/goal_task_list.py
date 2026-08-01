# (Coding Track)

# Exercise 4A  Goal → Task-List Decomposition    QUICK WIN

 

# Problem Statement:  Given a high-level goal, an agent returns an ordered, dependency-aware task list as JSON.

# Goal of the Problem:  See planning as goal decomposition and get reliable structured output.

 

# Step 1 —  Install the library and set your API key

# Run this once per session. Paste the OpenAI API key you were given.

# Python

# pip install openai --quiet

 

# Python

import os

os.environ["OPENAI_API_KEY"] = "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"

 

# Expected output

# # (No output. The key is now available to the OpenAI client.)

 

# # Step 2 —  Build a JSON planner and run it

# # Python

from openai import OpenAI

import json

client = OpenAI()

 

def planner(goal):

  r = client.chat.completions.create(

       model="gpt-4o-mini",

       response_format={"type": "json_object"},

       messages=[

         {"role": "system", "content":

           'Return JSON {"goal":..., "tasks":[{"id":1,"task":...,"depends_on":[]}]}. '

           'Use 3-6 ordered tasks.'},

         {"role": "user", "content": f"Goal: {goal}"}])

  return json.loads(r.choices[0].message.content)

 

plan = planner("Launch a monthly newsletter for our finance team")

print(json.dumps(plan, indent=2))

 

# Expected output

{

"goal": "Launch a monthly newsletter for our finance team",

"tasks": [

  {"id": 1, "task": "Define audience and goals", "depends_on": []},

  {"id": 2, "task": "Choose an email platform", "depends_on": [1]},

  {"id": 3, "task": "Design a template", "depends_on": [2]},

  {"id": 4, "task": "Draft the first issue", "depends_on": [3]},

  {"id": 5, "task": "Schedule and send", "depends_on": [4]}

]

}

# Task content varies, but you always get an ordered, dependency-aware plan.

 
