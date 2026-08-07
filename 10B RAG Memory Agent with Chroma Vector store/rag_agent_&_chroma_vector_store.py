# Exercise 7B  RAG Memory Agent with a Chroma Vector Store    DEEP DIVE

# Environment: Google Colab (Python + Chroma + OpenAI)     Est. time: 18 min

# Problem Statement:  Ingest a small knowledge base into a Chroma vector store, retrieve relevant chunks for a question, and have an agent answer using only that context — refusing to guess when the answer isn't there.

# Goal of the Problem:  Build the full Retrieval-Augmented Memory loop (ingest → retrieve → generate) on a real vector database.

 

# Step 1 —  Install Chroma

# Python

# !pip install chromadb openai --quiet

 

# Expected output

# Installs Chroma (an embeddable vector database) and the OpenAI client.

 

# Step 2 —  Build the vector store

# Python

import chromadb, os

from openai import OpenAI

os.environ["OPENAI_API_KEY"] = "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"
client = OpenAI()

 

docs = [

  "Our refund policy allows returns within 30 days with a receipt.",

  "The Premium plan costs $20 per month and includes priority support.",

  "Support hours are 9am-6pm IST, Monday to Friday.",

  "Customer data is encrypted at rest using AES-256.",

]

 

def embed(texts):

  return [d.embedding for d in client.embeddings.create(

      model="text-embedding-3-small", input=texts).data]

 

chroma = chromadb.Client()

col = chroma.create_collection("kbs")

col.add(ids=[f"d{i}" for i in range(len(docs))],

       documents=docs, embeddings=embed(docs))

print("Stored", col.count(), "documents")

 

# Expected output

# Stored 4 documents

# # A tiny knowledge base now lives in the Chroma vector store.

 

# Step 3 —  Retrieve and answer (grounded)

# Python

def rag_answer(question, k=2):

  qv = embed([question])[0]

  hits = col.query(query_embeddings=[qv], n_results=k)["documents"][0]

  context = "\n".join(hits)

  r = client.chat.completions.create(

       model="gpt-4o-mini",

       messages=[{"role": "system", "content":

                    "Answer ONLY from the context. If it is not there, say 'I don't have that info.'"},

                 {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}])

  return r.choices[0].message.content, hits

 

answer, hits = rag_answer("How much is the premium plan?")

print("Retrieved:", hits)

print("Answer:", answer)

print("\nUnknown question ->", rag_answer("What is your CEO's name?")[0])

 

# Expected output

# Retrieved: ['The Premium plan costs $20 per month and includes priority support.', ...]

# Answer: The Premium plan costs $20 per month and includes priority support.

 

# Unknown question -> I don't have that info.

# # The agent answers from retrieved memory and refuses to hallucinate when it can't.

 