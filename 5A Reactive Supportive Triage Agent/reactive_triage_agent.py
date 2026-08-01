import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# (Code based Track)

# Exercise 1A  Reactive Support-Triage Agent    QUICK WIN

# Environment: Google Colab (pure Python)    Est. time: 5 min

# Problem Statement:  Build a reactive agent that instantly routes an incoming customer message to the right support queue using simple condition→action rules — no memory, no planning.

# Goal of the Problem:  Feel the reactive paradigm (perception → immediate action) and discover where it breaks down.

 

# Step 1 —  Open a new Colab notebook

# Go to colab.research.google.com → New notebook. No installs are needed for this one.

# Step 2 —  Define the reactive agent

# Python

def reactive_agent(message: str) -> str:

  text = message.lower()

  # condition -> action rules, checked top to bottom (no memory, no planning)

  rules = [

       (lambda t: any(w in t for w in ["refund", "money back", "charge"]), "BILLING_QUEUE"),

       (lambda t: any(w in t for w in ["password", "login", "sign in", "reset"]), "ACCOUNT_QUEUE"),

       (lambda t: any(w in t for w in ["crash", "error", "bug", "broken"]), "TECH_QUEUE"),

       (lambda t: any(w in t for w in ["cancel", "unsubscribe"]), "RETENTION_QUEUE"),

  ]

  for condition, action in rules:

       if condition(text):

           return action

  return "GENERAL_QUEUE"  # default reflex

 

# Expected output

# (No output yet - this just defines the function.)

 

# Step 3 —  Test it on sample messages

# Python

tests = [

  "I want a refund for last month's charge",

  "I can't login, need to reset my password",

  "The app keeps crashing with an error",

  "How do I change my profile picture?",

]

for m in tests:

  print(f"{reactive_agent(m):15} <- {m}")

 

# Expected output

# BILLING_QUEUE   <- I want a refund for last month's charge

# ACCOUNT_QUEUE   <- I can't login, need to reset my password

# TECH_QUEUE      <- The app keeps crashing with an error

# GENERAL_QUEUE   <- How do I change my profile picture?

 

# Step 4 —  Find the limitation

# Reactive agents can't weigh context. Watch what happens with an ambiguous message.

# Python

# A tricky message that contains BOTH "charge" and "cancel":

print(reactive_agent("I was charged after I cancelled my plan"))

 

# Expected output

# BILLING_QUEUE

# # The first matching rule wins. A reactive agent cannot weigh context or

# # realise this is really a cancellation dispute - that needs deliberation.