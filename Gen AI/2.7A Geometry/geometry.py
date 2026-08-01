import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Hands-On 7A · Quick Win — Meaning as Geometry

# Problem Statement:  You keep hearing that embeddings 'capture meaning', but it sounds like magic. You want to see two differently-worded sentences score as similar and an unrelated one score as distant.

# Goal of the Problem: Embed a few sentences with text-embedding-3-small and use cosine similarity to measure how close their meanings are.

# Where to run: VS Code or Colab  ·   Est. time: 15 min   ·  Concepts: embeddings, cosine similarity

# Step 1 — Write helper functions to embed and compare

import numpy as np

 

def embed(texts):

   r = client.embeddings.create(model="text-embedding-3-small", input=texts)

   return np.array([d.embedding for d in r.data])

 

def cosine(a, b):

  return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

# Expected output

# # defines embed() and cosine(); no output

# Step 2 — Embed sentences and check the vector size

sentences = [

   "How do I reset my password?",     # 0

   "I forgot my login credentials",   # 1  (same meaning, different words)

   "What time does the branch close?",# 2  (unrelated)

]

vecs = embed(sentences)

print("Vectors shape:", vecs.shape)   # (rows, dimensions)

# Expected output

# Vectors shape: (3, 1536)

# Step 3 — Compare meanings

print("sim(0,1) reset vs forgot login :", round(cosine(vecs[0], vecs[1]), 3))

print("sim(0,2) reset vs branch hours  :", round(cosine(vecs[0], vecs[2]), 3))

# Expected output

# sim(0,1) reset vs forgot login : 0.71

# sim(0,2) reset vs branch hours  : 0.18

# (exact numbers vary slightly, but 0,1 will be clearly higher than 0,2)

# Takeaway:  Similar meaning = closer vectors, even with no shared words. That single idea is the engine under semantic search and RAG.