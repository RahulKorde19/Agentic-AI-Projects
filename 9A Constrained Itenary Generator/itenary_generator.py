# (Code Base)

# Exercise 6A  Constrained Itinerary Generator    QUICK WIN

 

# Problem Statement:  Given a destination, number of days, budget and interests, produce a day-by-day itinerary that respects the budget.

# Goal of the Problem:  Practise constraint-aware structured generation and verify the constraint programmatically.

 

# Step 1 —  Install the library and set your API key

# Run this once per session. Paste the OpenAI API key you were given.

# Python

# !pip install openai --quiet

 

# Python

import os

os.environ["OPENAI_API_KEY"] = "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"

 

# Expected output

# (No output. The key is now available to the OpenAI client.)

 

# Step 2 —  Build the travel planner and check the budget

# Python

from openai import OpenAI

import json

client = OpenAI()

 

def travel_planner(dest, days, budget_usd, interests):

  r = client.chat.completions.create(

       model="gpt-4o-mini", response_format={"type": "json_object"},

       messages=[{"role": "system", "content":

           'Return JSON {"destination":...,"days":[{"day":1,"morning":...,'

          '"afternoon":...,"evening":...,"est_cost_usd":int}],'

          '"total_est_cost_usd":int}. Stay within the budget.'},

                 {"role": "user", "content":

           f"Dest:{dest} Days:{days} Budget(USD):{budget_usd} Interests:{interests}"}])

  return json.loads(r.choices[0].message.content)

 

plan = travel_planner("Lisbon", 3, 600, ["food", "history", "budget-friendly"])

print(json.dumps(plan, indent=2))

print("Within budget?", plan["total_est_cost_usd"] <= 600)

 

# Expected output

{

"destination": "Lisbon",

"days": [

  {"day": 1, "morning": "Explore Alfama", "afternoon": "Sao Jorge Castle",

    "evening": "Fado dinner", "est_cost_usd": 180},

  {"day": 2, "...": "..."},

  {"day": 3, "...": "..."}

],

"total_est_cost_usd": 560

}

# Within budget? True

# A constraint-aware, day-by-day itinerary under the $600 budget.

 
