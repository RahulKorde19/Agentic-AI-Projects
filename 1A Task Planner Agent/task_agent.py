import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Quick Win 1A: The Task-Planner Agent

# Quick Win  • ~15 minutes

# Problem Statement: Given a fuzzy, one-line goal, produce a short, ordered list of concrete steps a person (or another agent) could follow.

 

# Goal of the Problem: See that the simplest 'agent' is just an LLM given a role and asked to decompose a goal into an actionable plan. This is the 'planning' capability of an agent.

 

# Step 1.  Install the OpenAI SDK (skip if already installed).

# pip install openai

 

# Expected output

# Successfully installed openai-1.x.x

 

# Step 2.  Create the client. (Your key is already in the environment from setup.)

from openai import OpenAI

client = OpenAI()

 

# Expected output

# (no output — the client is ready)

 

# Step 3.  Write a planning function. The system message gives the model its 'role'.

def make_plan(goal: str) -> str:

   response = client.chat.completions.create(

       model="gpt-4o-mini",

       messages=[

           {"role": "system", "content":

            "You are a planning agent. Break the user's goal into a short, "

            "ordered list of concrete, actionable steps. Return 4-6 steps only."},

           {"role": "user", "content": goal},

       ],

   )

   return response.choices[0].message.content

 

# Expected output

# (no output — the function is defined)

 

# Step 4.  Run it on a real goal.

print(make_plan(

   "Organize a 2-hour team knowledge-sharing session on Agentic AI"))

 

# Expected output

# 1. Define the session objective and who should attend.

# 2. Pick 3-4 key subtopics and assign time to each.

# 3. Prepare a short live demo and one hands-on exercise.

# 4. Book the room / video call and send an agenda invite.

# 5. Gather feedback with a quick survey afterwards.

# (exact wording will vary each run)

 

# Step 5.  Now make it yours — swap in a goal from your own work and re-run.

print(make_plan("<type your own goal here>"))

 

# Expected output

# A fresh 4-6 step plan tailored to your goal.

 

 
