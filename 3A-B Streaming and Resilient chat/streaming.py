import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



# Problem Statement: Users hate staring at a spinner while a long answer generates. You want text to appear as it is produced, the way ChatGPT does.

# Goal of the Problem: Stream a chat completion and print tokens as they arrive, using clean environment setup (no hard-coded key).

# Where to run: VS Code or Colab

# Concepts: streaming, partial output, env hygiene

# Step 1 — Confirm your client is wired up

# You should already have client from the setup section. Quick sanity check:

print("Key loaded:", bool(client.api_key))

# Expected output

# Key loaded: True

# Step 2 — Stream a response

# Set stream=True. Instead of one response object you now iterate over chunks; each chunk carries a small delta of text.

stream = client.chat.completions.create(

   model="gpt-4.1-mini",

   messages=[

       {"role": "system", "content": "You are a concise banking assistant."},

       {"role": "user",   "content": "List 3 quick tips to improve my credit score."},

   ],

   stream=True,

)

 

for chunk in stream:

   delta = chunk.choices[0].delta.content

   if delta:

       print(delta, end="", flush=True)

print()

# Expected output

# 1. Pay every bill on time — payment history matters most.

# 2. Keep credit-card usage below 30% of your limit.

# 3. Avoid applying for many new loans at once.

# (text appears progressively, a few characters at a time)

# Step 3 — Reassemble the full text while streaming

# Often you want to show text live AND keep the complete string. Collect the deltas:

stream = client.chat.completions.create(

   model="gpt-4.1-mini",

   messages=[{"role": "user", "content": "Give me one motivational line about saving money."}],

   stream=True,

)

 

full = ""

for chunk in stream:

   delta = chunk.choices[0].delta.content or ""

   full += delta

   print(delta, end="", flush=True)

 

print("\n\nCaptured length:", len(full), "characters")

# Expected output

# Every rupee you save today is a choice your future self will thank you for.

 

# Captured length: 73 characters

# Takeaway:  Streaming does not change what the model says — only how you receive it. You handle partial output yourself and decide when to render it.