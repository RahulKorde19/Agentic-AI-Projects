import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Problem Statement: A colleague insists the model 'says something different every time'. You need to show when that is true, when it isn't, and which knob controls it.

# Goal of the Problem: Call the Chat Completions endpoint at low and high temperature and watch determinism vs variety with your own eyes.

# Where to run: VS Code or Colab 

# Step 1 — Make your first Chat Completions call

# A request is a list of messages with roles. The system message sets behaviour; the user message is the request.

resp = client.chat.completions.create(

   model="gpt-4.1-mini",

   messages=[

       {"role": "system", "content": "You are a concise banking marketing assistant."},

       {"role": "user",   "content": "Write a one-line tagline for a new savings account."},

   ],

   temperature=0,

   max_tokens=30,

)

print(resp.choices[0].message.content.strip())

# Expected output

# "Grow your savings, secure your future — start today."

# (your exact wording will differ, but it will be a single tagline)

# Step 2 — Compare low vs high temperature, twice each

def tagline(temp):

   r = client.chat.completions.create(

       model="gpt-4.1-mini",

       messages=[

           {"role": "system", "content": "You are a concise banking marketing assistant."},

           {"role": "user",   "content": "Write a one-line tagline for a new savings account."},

       ],

       temperature=temp,

       max_tokens=30,

   )

   return r.choices[0].message.content.strip()

 

for temp in [0.0, 0.0, 1.0, 1.0]:

  print(f"temp={temp}: {tagline(temp)}")

# Expected output

# temp=0.0: Grow your savings, secure your future — start today.

# temp=0.0: Grow your savings, secure your future — start today.

# temp=1.0: Watch every rupee bloom into tomorrow's peace of mind.

# temp=1.0: Your money, wide awake and working while you rest.

 
