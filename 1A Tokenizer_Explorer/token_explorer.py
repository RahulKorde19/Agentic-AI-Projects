######## Step 1: Setup


import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print(client)

##############################################################################
#####Step 2: Tokenization
# Problem Statement: Your team keeps hitting surprise costs and truncated prompts, but nobody can say how many tokens a piece of text actually uses. You need to see, concretely, how text becomes tokens.

# Goal of the Problem: Turn a sentence into tokens with tiktoken, count them, and see the sub-word pieces — so 'tokens' stop being an abstraction.

# Where to run: VS Code or Colab  ·   Est. time: 10 min   ·  Concepts: tokens, tokenisation

# Step 1 — Encode text into tokens

# tiktoken is OpenAI's tokenizer. The GPT-4.1 / GPT-4o family uses the o200k_base encoding.


import tiktoken

enc = tiktoken.get_encoding("o200k_base")

text = "Generative AI is transforming banking operations."

tokens = enc.encode(text)

 

print("Text          :", text)

print("Token count   :", len(tokens))

print("Token IDs     :", tokens)


####################################################
# Step 3:
#  See the actual sub-word pieces

# Decode each token individually to reveal how words are broken up:

pieces = [enc.decode([t]) for t in tokens]

print("Pieces        :", pieces)

############################################################
# Step 4 — Compare short vs long text

short = "Balance?"

long  = "Please summarise the last twelve months of transactions for this account."

for label, s in [("short", short), ("long", long)]:

  print(f"{label:6s} words={len(s.split()):2d}  tokens={len(enc.encode(s)):2d}")

