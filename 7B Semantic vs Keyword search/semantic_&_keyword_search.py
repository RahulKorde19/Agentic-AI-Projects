import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Hands-On 7B · Stretch — Semantic vs Keyword Search

# Problem Statement: Your current help-search matches keywords, so 'my card won't work when I pay' returns nothing useful because the help article says 'declined at a shop'. You want to show where semantic search wins.

# Goal of the Problem: Build a tiny corpus and run both a keyword search and a semantic search on the same query, and compare the top result of each.

# Where to run: VS Code or Colab  ·   Est. time: 25 min   ·  Concepts: semantic vs keyword search

# Step 1 — Create a small help corpus

import numpy as np

 

corpus = [

   "To block a lost debit card, call our 24x7 helpline or use the app.",

   "Savings account minimum balance is 5000 rupees in metro branches.",

   "If your card is declined at a shop, check your daily transaction limit.",

   "Home loan foreclosure has no penalty for floating-rate loans.",

]

 

def embed(texts):

   r = client.embeddings.create(model="text-embedding-3-small", input=texts)

   return np.array([d.embedding for d in r.data])

 

def cosine(a, b):

  return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

# Expected output

# # defines corpus, embed(), cosine(); no output

# Step 2 — Keyword search (word overlap)

query = "my card won't work when I pay"

q_words = set(query.lower().replace("'", "").split())

 

kw_ranked = sorted(

   [(len(q_words & set(doc.lower().split())), doc) for doc in corpus],

   reverse=True,

)

print("KEYWORD top overlap:", kw_ranked[0][0], "words")

print("KEYWORD top result :", kw_ranked[0][1])

# Expected output

# KEYWORD top overlap: 1 words

# KEYWORD top result : To block a lost debit card, call our 24x7 helpline or use the app.

# Keyword search latches onto the shared word 'card' and returns the blocking article — not the one about a card being declined at payment.

# Step 3 — Semantic search (cosine over embeddings)

corpus_vecs = embed(corpus)

q_vec = embed([query])[0]

 

sem_ranked = sorted(

   [(cosine(q_vec, corpus_vecs[i]), corpus[i]) for i in range(len(corpus))],

   reverse=True,

)

print("SEMANTIC top score :", round(sem_ranked[0][0], 3))

print("SEMANTIC top result:", sem_ranked[0][1])

# Expected output

# SEMANTIC top score : 0.52

# SEMANTIC top result: If your card is declined at a shop, check your daily transaction limit.

# Takeaway:  Keyword search matches strings; semantic search matches meaning. For natural-language questions that rarely reuse the exact words in your docs, semantic retrieval wins — which is why RAG is built on it.