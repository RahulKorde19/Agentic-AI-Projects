

# Exercise 8A  Agent with Short-term + Long-term Memory    

 

# Problem Statement:  Build an agent with a short-term rolling buffer (recent turns) and a long-term vector memory (persisted facts), then show it recall a fact after short-term memory is wiped.

# Goal of the Problem:  Distinguish short-term from long-term memory and see retrieval-augmented recall in action.

 

# Step 1 —  Install Chroma

# Python

# pip install chromadb openai --quiet

 

# Expected output

# Installs Chroma (an embeddable vector database) and the OpenAI client.

 

# Step 2 —  Define both memory stores

# Python

import chromadb

from collections import deque

from openai import OpenAI

client = OpenAI()

 

def embed(t):

  return client.embeddings.create(model="text-embedding-3-small", input=[t]).data[0].embedding

 

col = chromadb.Client().create_collection("ltm")

_next_id = [0]

 

def remember(fact):                       # write to LONG-TERM memory

  _next_id[0] += 1

  col.add(ids=[str(_next_id[0])], documents=[fact], embeddings=[embed(fact)])

 

def recall(query, k=2):                    # read from LONG-TERM memory

  if col.count() == 0:

       return []

  n = min(k, col.count())

  return col.query(query_embeddings=[embed(query)], n_results=n)["documents"][0]

 

short_term = deque(maxlen=4)               # SHORT-TERM memory: last 4 turns only

 

# Expected output

# (No output - defines short-term buffer + long-term vector memory.)

 

# Step 3 —  Build the memory-augmented agent

# Python

def agent(user_msg):

  # naive rule: if the user states something about themselves, store it long-term

  if user_msg.lower().startswith(("my ", "i ")):

       remember(user_msg)

  ltm = "\n".join(recall(user_msg)) or "(nothing)"

  stm = "\n".join(short_term) or "(nothing)"

  r = client.chat.completions.create(

       model="gpt-4o-mini",

       messages=[{"role": "system", "content": "Use long-term memory and recent turns to answer personally."},

                 {"role": "user", "content":

                    f"Long-term memory:\n{ltm}\nRecent turns:\n{stm}\n\nUser: {user_msg}"}])

  reply = r.choices[0].message.content

  short_term.append(f"User: {user_msg}")

  short_term.append(f"Agent: {reply}")

  return reply

 

# Expected output

# (No output - the memory-augmented agent.)

 

# Step 4 —  Prove recall survives a session reset

# Python

print(agent("My name is Priya and I love mango lassi."))

print(agent("I work as a data analyst at a bank."))

 

short_term.clear()          # wipe SHORT-TERM memory (simulate a new session)

 

print(agent("What drink do I like, and what is my job?"))

 

# Expected output

# Nice to meet you, Priya! Mango lassi is a great choice.

# Got it - a data analyst at a bank.

# You like mango lassi, and you work as a data analyst at a bank.

# # Even after short-term memory is cleared, the agent recalls the facts from

# # LONG-TERM (vector) memory - exactly how persistent agent memory works.