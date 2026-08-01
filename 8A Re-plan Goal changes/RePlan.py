

# Exercise 5A  Re-plan When the Goal Changes    QUICK WIN

 

# Problem Statement:  Generate a plan, then inject a new constraint and have the agent produce a revised plan that explains what it changed.

# Goal of the Problem:  See adaptive planning — agents updating plans when goals or constraints shift.

 

# Step 1 —  Install the library and set your API key

# Run this once per session. Paste the OpenAI API key you were given.

# Python

# pip install openai --quiet

 

# Python

import os

os.environ["OPENAI_API_KEY"] = "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"

 

# Expected output

# (No output. The key is now available to the OpenAI client.)

 

# Step 2 —  Make the original plan

# Python

from openai import OpenAI

import json

client = OpenAI()

 

def make_plan(goal, constraints):

  r = client.chat.completions.create(

       model="gpt-4o-mini", response_format={"type": "json_object"},

       messages=[{"role": "system", "content": 'Return JSON {"steps":[...]} that respects all constraints.'},

                 {"role": "user", "content": f"Goal: {goal}\nConstraints: {constraints}"}])

  return json.loads(r.choices[0].message.content)

 

plan = make_plan("Organize a team offsite", ["budget $2000", "1 day", "20 people"])

print("ORIGINAL PLAN:")

print(json.dumps(plan, indent=2))

 

# Expected output

# ORIGINAL PLAN:

{

"steps": [

  "Book a local venue with catering",

  "Arrange team-building activities",

  "Organise transport for 20 people",

  "Send invites and agenda"

]

}

# An in-person plan within the original constraints.

 

# Step 3 —  Revise the plan for a new constraint

# Python

def revise_plan(old_plan, change):

  r = client.chat.completions.create(

       model="gpt-4o-mini", response_format={"type": "json_object"},

       messages=[{"role": "system", "content":

                    'Given an existing plan and a change, return JSON '

                   '{"changed":["...what you altered and why..."],"steps":["...new plan..."]}'},

                 {"role": "user", "content": f"Existing plan: {json.dumps(old_plan)}\nChange: {change}"}])

  return json.loads(r.choices[0].message.content)

 

revised = revise_plan(plan, "Budget cut to $800 and it must now be fully virtual")

print(json.dumps(revised, indent=2))

 

# Expected output

{

"changed": [

  "Dropped venue and transport - event is now virtual",

  "Replaced catering with a small food-delivery stipend to fit $800"

],

"steps": [

  "Set up a video-conferencing room",

  "Plan online team-building games",

  "Send each person a $20 lunch voucher",

  "Share agenda and joining link"

]

}

# The agent explains what it CHANGED and produces a new within-constraint plan.

 
