import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# RAG

# (Code Based) 

# Hands-on 1-A  (Quick Win): Find the closest sentence by meaning

# Problem Statement: You have a user question and four candidate sentences. Find which candidate is closest in meaning to the question — even when they share almost no words.

# Goal of the Problem: See first-hand that embeddings capture meaning (not keywords), and learn to score similarity with cosine similarity — the single most important operation in RAG.

# Step 1. Install the embedding library

#  CODE — copy & paste

# !pip install -q sentence-transformers (for Google Collab)

# pip install sentence-transformers (for VS Code) 

#  EXPECTED OUTPUT

# Installing collected packages: ... sentence-transformers

# (a few dependency lines, then the cell finishes with no error)

# Step 2. Load a small, fast embedding model

#  CODE — copy & paste

from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

print('Embedding dimension:', model.get_sentence_embedding_dimension())

#  EXPECTED OUTPUT

# (first run downloads ~90 MB)

# Embedding dimension: 384

# Step 3. Turn four sentences into vectors

#  CODE — copy & paste

sentences = [

   'How do I reset my password?',

   'The cat napped on the warm windowsill.',

   'Steps to recover a forgotten login credential.',

   'Our office is closed on public holidays.',

]

embeddings = model.encode(sentences)

print('Shape:', embeddings.shape)

#  EXPECTED OUTPUT

# Shape: (4, 384)

# Step 4. Score a query against all four

#  CODE — copy & paste

from sentence_transformers import util

query = "I can't remember my account password"

q_emb = model.encode(query)

scores = util.cos_sim(q_emb, embeddings)[0]

ranked = sorted(zip(sentences, scores), key=lambda x: x[1], reverse=True)

for text, score in ranked:

   print(f'{score:.3f}  | {text}')

#  EXPECTED OUTPUT

# 0.71  |  How do I reset my password?

# 0.58  | Steps to recover a forgotten login credential.

# 0.06  |  Our office is closed on public holidays.

# 0.02  |  The cat napped on the warm windowsill.

# 💡 Notice the winner shares the word 'password', but the runner-up ('recover a forgotten login credential') shares NO keywords with the query — yet still scores high. That is semantic search. Keyword search would have missed it.