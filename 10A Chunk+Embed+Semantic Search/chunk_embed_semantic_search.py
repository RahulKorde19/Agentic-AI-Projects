# (Code Based)

# Exercise 7A  Chunk + Embed + Semantic Search (from scratch)    QUICK WIN

 

# Problem Statement:  Split a document into overlapping chunks, embed them, and retrieve the chunks most similar to a query — using only numpy for the maths.

# Goal of the Problem:  Understand chunking, embeddings and cosine similarity from first principles, with no vector DB hiding the mechanics.

 

# Step 1 —  Install the library and set your API key

# Run this once per session. Paste the OpenAI API key you were given.

# Python

# pip install openai --quiet

 

# Python

import os

os.environ["OPENAI_API_KEY"] = "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"

 

# Expected output

# (No output. The key is now available to the OpenAI client.)

 

# Step 2 —  Add a document and a chunker

# Python

document = """Agents can store information in two ways. Short-term memory holds the

current conversation and is lost when the session ends. Long-term memory persists

across sessions and is usually implemented with a vector store. To build long-term

memory we split documents into chunks, convert each chunk into an embedding, and

save those embeddings. At query time we embed the question and use semantic

similarity to find the most relevant chunks. This retrieval step is the core of

Retrieval Augmented Generation, where retrieved chunks are added to the prompt so

the model can answer using knowledge it was never trained on."""

 

def chunk_text(text, size=40, overlap=8):

  words = text.split()

  chunks, i = [], 0

  while i < len(words):

       chunks.append(" ".join(words[i:i + size]))

       i += size - overlap

  return chunks

 

chunks = chunk_text(document)

print(f"{len(chunks)} chunks created")

 

# Expected output

# 3 chunks created

# # The document is split into overlapping windows so no idea is cut in half.

 

# Step 3 —  Embed the chunks

# Python

from openai import OpenAI

import numpy as np

client = OpenAI()

 

def embed(texts):

  r = client.embeddings.create(model="text-embedding-3-small", input=texts)

  return [d.embedding for d in r.data]

 

chunk_vecs = embed(chunks)

print("Embedded", len(chunk_vecs), "chunks, each of length", len(chunk_vecs[0]))

 

# Expected output

# Embedded 3 chunks, each of length 1536

# # Each chunk is now a 1536-dimension vector.

 

# Step 4 —  Search by cosine similarity

# Python

def cosine(a, b):

  a, b = np.array(a), np.array(b)

  return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

 

def search(query, k=2):

  qv = embed([query])[0]

  scored = sorted(((cosine(qv, v), c) for v, c in zip(chunk_vecs, chunks)), reverse=True)

  return scored[:k]

 

for score, chunk in search("How do agents keep memory across sessions?"):

  print(round(score, 3), "->", chunk[:70], "...")

 

# Expected output

# 0.612 -> Long-term memory persists across sessions and is usually implemented ...

# 0.404 -> ... To build long-term memory we split documents into chunks ...

# # The chunk about long-term memory scores highest - semantic search in ~20 lines.

 

