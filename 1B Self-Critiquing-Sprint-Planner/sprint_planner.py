

import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Challenge 1B: The Self-Critiquing Sprint Planner

# Challenge  •  ~30 minutes

# Problem Statement: A single-shot plan is often shallow. Build an agent that drafts a plan, critiques its own draft for risks and gaps, and then produces an improved plan.

 

# Goal of the Problem: Implement the Reflection pattern (generate → critique → revise) — one of the core agentic loops. You will feel the quality jump between the draft and the revised plan.

 

# Step 1.  A small helper so we can call the model repeatedly with different roles.

def ask(system: str, user: str) -> str:

   r = client.chat.completions.create(

       model="gpt-4o-mini",

       messages=[{"role": "system", "content": system},

                 {"role": "user", "content": user}],

   )

   return r.choices[0].message.content

 

# Expected output

# (no output — helper defined)

 

# Step 2.  Step 1 of the loop — draft an initial plan.

goal = ("Plan a 3-week sprint to migrate 200 GB of customer data to a new "

       "warehouse with zero downtime.")

 

draft = ask("You are a project planning agent. Produce a concise sprint plan "

           "as a numbered list.", goal)

print("DRAFT PLAN:\n", draft)

 

# Expected output

# DRAFT PLAN:

# 1. Week 1: audit current schema...

# 2. Week 2: build ETL...

# 3. Week 3: cutover and validate...

# (a reasonable but incomplete plan)

 

# Step 3.  Step 2 of the loop — the agent critiques its own plan.

critique = ask(

   "You are a critical reviewer. List concrete risks, gaps, and missing "

   "steps in the plan. Be specific.",

   f"Goal: {goal}\n\nPlan:\n{draft}")

print("CRITIQUE:\n", critique)

 

# Expected output

# CRITIQUE:

# - No rollback / backup strategy mentioned.

# - Missing data-validation and reconciliation step.

# - No stakeholder sign-off or communication plan.

# - 'Zero downtime' not addressed (needs dual-write / shadow reads).

 

# Step 4.  Step 3 of the loop — revise the plan to fix every issue raised.

final = ask(

   "You are a planning agent. Rewrite the plan so it fixes every issue in "

   "the critique. Return the improved numbered plan only.",

   f"Goal: {goal}\n\nOriginal plan:\n{draft}\n\nCritique:\n{critique}")

print("IMPROVED PLAN:\n", final)

 

# Expected output

# IMPROVED PLAN:

# A richer plan that now includes a backup/rollback step,

# a dual-write cutover for zero downtime, validation & reconciliation,

# and a stakeholder communication checkpoint.

 

# Step 5.  Reflect: you just built a 3-node agent loop by hand. Notice the improved plan is materially better because the agent reviewed its own work — the same idea powers self-correcting agents.

 