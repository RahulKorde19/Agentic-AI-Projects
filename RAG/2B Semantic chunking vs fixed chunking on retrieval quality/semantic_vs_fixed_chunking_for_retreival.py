
import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Problem Statement: Fixed-size chunks can split a single idea across two chunks, hurting retrieval. Use semantic chunking (split where meaning shifts) and compare which strategy retrieves the better passage for a tricky query.

# Goal of the Problem: Connect a chunking choice directly to retrieval quality, and learn when semantic chunking is worth its extra cost.

# Step 1. Install the libraries

#  CODE — copy & paste

# !pip install -q langchain-experimental langchain-huggingface sentence-transformers

#  EXPECTED OUTPUT

# (installs quietly)

# Step 2. A multi-topic document and an embedding function

#  CODE — copy & paste

from langchain_huggingface import HuggingFaceEmbeddings

emb = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

 

doc = (

 'The refund window is 30 days from purchase. Refunds go to the original card. '

 'Our data centres run entirely on renewable energy since 2023. '

 'We offset remaining emissions through verified reforestation projects. '

'Enterprise plans include a dedicated account manager and 24x7 support. '

 'SLA guarantees 99.9 percent uptime with service credits for breaches.'

)

#  EXPECTED OUTPUT

# (model loads; no printed output)

# Step 3. Fixed-size chunks

#  CODE — copy & paste

from langchain_text_splitters import RecursiveCharacterTextSplitter

fixed = RecursiveCharacterTextSplitter(chunk_size=90, chunk_overlap=0).split_text(doc)

print('Fixed chunks:', len(fixed))

for ch in fixed: print(' -', ch)

#  EXPECTED OUTPUT

# Fixed chunks: 5-6

# - (chunks that may cut the 'renewable energy / offset emissions' idea apart)

# Step 4. Semantic chunks (split where meaning shifts)

#  CODE — copy & paste

from langchain_experimental.text_splitter import SemanticChunker

semantic = SemanticChunker(emb).split_text(doc)

print('Semantic chunks:', len(semantic))

for ch in semantic: print(' -', ch)

#  EXPECTED OUTPUT

# Semantic chunks: 3-4

# - The refund window is 30 days from purchase. Refunds go to the original card.

# - Our data centres run entirely on renewable energy since 2023. We offset remaining emissions through verified reforestation projects.

# - Enterprise plans include a dedicated account manager and 24x7 support. SLA guarantees 99.9 percent uptime ...

# (related sentences about sustainability now sit together in ONE chunk)

# Step 5. Compare retrieval for a tricky query

#  CODE — copy & paste

from sentence_transformers import SentenceTransformer, util

m = SentenceTransformer('all-MiniLM-L6-v2')

query = 'how does the company handle its carbon footprint?'

q = m.encode(query, convert_to_tensor=True)

 

for name, chunks in [('FIXED', fixed), ('SEMANTIC', semantic)]:

   ce = m.encode(chunks, convert_to_tensor=True)

   top = util.semantic_search(q, ce, top_k=1)[0][0]

   print(name, '->', round(top['score'],3), chunks[top['corpus_id']][:80])

#  EXPECTED OUTPUT

# FIXED    -> 0.41 Our data centres run entirely on renewable energy since 2023.

# SEMANTIC -> 0.55 Our data centres run entirely on renewable energy since 2023. We offset ...

# (the semantic chunk returns the FULL answer — energy + offsets — in one retrieved piece)

 