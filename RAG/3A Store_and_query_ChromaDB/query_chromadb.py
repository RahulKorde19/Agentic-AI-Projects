import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Hands-on 3-A : Store and query with ChromaDB

# Problem Statement: Replace your hand-rolled numpy search with a real vector database. Add documents to ChromaDB and run a similarity query — letting the database handle the embedding and the math.

# Goal of the Problem: Get comfortable with the add / query loop of a vector DB, and read distances (lower = closer).

# Step 1. Install ChromaDB

#  CODE — copy & paste

# !pip install -q chromadb (for Google Collab) 

# pip install –q chromadb (for VS Code) 

#  EXPECTED OUTPUT

# (installs quietly)

# Step 2. Create an in-memory client and a collection

#  CODE — copy & paste

import chromadb

client = chromadb.Client()

collection = client.create_collection(name='faq')

print('Collection ready:', collection.name)

#  EXPECTED OUTPUT

# Collection ready: faq

# Step 3. Add documents (Chroma embeds them automatically)

#  CODE — copy & paste

collection.add(

  documents=[

      'Click Forgot Password on the login page to reset it.',

      'Refunds take 5-7 business days to the original card.',

      'Support hours are 9am to 6pm IST, Monday to Friday.',

      'Enable two-factor authentication in Security settings.',

   ],

  ids=['d1', 'd2', 'd3', 'd4'],

)

print('Documents stored:', collection.count())

#  EXPECTED OUTPUT

# (first call downloads the default MiniLM embedder)

# Documents stored: 4

# Step 4. Query by meaning

#  CODE — copy & paste

res = collection.query(query_texts=['I forgot my password'], n_results=2)

for doc, dist in zip(res['documents'][0], res['distances'][0]):

   print(round(dist, 3), doc)

#  EXPECTED OUTPUT

# 0.42 Click Forgot Password on the login page to reset it.

# 1.35 Enable two-factor authentication in Security settings.

# (lower distance = more relevant; the password doc wins clearly)

 