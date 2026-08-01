import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



# (Coding Track)

# Exercise 2A  Writer → Editor Hand-off    QUICK WIN

 

# Problem Statement:  Draft then improve a short LinkedIn post using two agents: a Writer produces a draft; an Editor critiques and rewrites it.

# Goal of the Problem:  See multi-agent collaboration — role specialisation and hand-off — with no framework at all.

 

# Step 1 —  Install the library and set your API key

# Run this once per session. Paste the OpenAI API key you were given.

# Python

# !pip install openai --quiet

 

# Python

import os

os.environ["OPENAI_API_KEY"] = "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"

 

# Expected output

# (No output. The key is now available to the OpenAI client.)

 

# Step 2 —  Create the Writer agent

# Python

from openai import OpenAI

client = OpenAI()

 

def writer_agent(topic):

  r = client.chat.completions.create(

       model="gpt-4o-mini",

       messages=[

         {"role": "system", "content": "You are a Writer. Write a punchy 4-sentence LinkedIn post."},

         {"role": "user", "content": f"Topic: {topic}"}])

  return r.choices[0].message.content

 

# Expected output

# (No output - defines the Writer agent.)

 

# Step 3 —  Create the Editor agent

# Python

def editor_agent(draft):

  r = client.chat.completions.create(

       model="gpt-4o-mini",

       messages=[

         {"role": "system", "content": "You are a strict Editor. Improve clarity, cut fluff, keep it under 60 words. Return ONLY the edited post."},

         {"role": "user", "content": f"Edit this:\n{draft}"}])

  return r.choices[0].message.content

 

# Expected output

# (No output - defines the Editor agent.)

 

# Step 4 —  Orchestrate the hand-off

# Python

topic = "Why every analyst should learn about AI agents"

draft = writer_agent(topic)

print("=== DRAFT (Writer) ===")

print(draft)

final = editor_agent(draft)

print("\n=== FINAL (Editor) ===")

print(final)

 

# Expected output

# === DRAFT (Writer) ===

# Curious about the future of work? AI agents are quietly reshaping how analysts

# operate ... (a 4-sentence draft appears here)

 

# === FINAL (Editor) ===

# AI agents are reshaping analytics. They automate the busywork, surface insights

# faster, and free you for the judgement calls only humans make. Learn them now -

# your future self will thank you.

# Exact wording varies each run; note how the Editor tightens the Writer's draft.

 
