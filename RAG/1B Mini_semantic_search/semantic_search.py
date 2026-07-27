import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Hands-on 1-B  (Challenge): Build a mini semantic search engine

# Problem Statement: Your support team keeps a small FAQ knowledge base. Build a reusable search(query, k) function that returns the top-k most relevant FAQ entries, ranked with scores — the 'retriever' that every RAG system is built on.

# Goal of the Problem: Convert the one-off similarity check from 1-A into a reusable retrieval function over a corpus, and confirm it returns sensible results for several different queries.

# Step 1. Load the model and define the knowledge base

#  CODE — copy & paste

from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

 

kb = [

   'To reset your password, click Forgot Password on the login page.',

  'Refunds are processed within 5-7 business days to the original card.',

   'Our support hours are 9am to 6pm IST, Monday to Friday.',

   'You can change your subscription plan under Settings > Billing.',

  'Download invoices from the Billing History section of your account.',

  'Two-factor authentication can be enabled in Security settings.',

   'Data is encrypted in transit and at rest using AES-256.',

   'To cancel, go to Settings > Subscription and choose Cancel Plan.',

]

print('Documents in KB:', len(kb))

#  EXPECTED OUTPUT

# Documents in KB: 8

# Step 2. Pre-compute embeddings once (this is your 'index')

#  CODE — copy & paste

kb_embeddings = model.encode(kb, convert_to_tensor=True)

print('Index shape:', kb_embeddings.shape)

#  EXPECTED OUTPUT

# Index shape: torch.Size([8, 384])

# Step 3. Write the reusable retriever

#  CODE — copy & paste

def search(query, k=3):

   q_emb = model.encode(query, convert_to_tensor=True)

   hits = util.semantic_search(q_emb, kb_embeddings, top_k=k)[0]

   results = []

   for h in hits:

      results.append((round(h['score'], 3), kb[h['corpus_id']]))

   return results

#  EXPECTED OUTPUT

# (no output — this cell just defines the function)

# Step 4. Try it with several queries

#  CODE — copy & paste

for q in ['how do I get my money back?',

        'when can I reach you?',

        'I want to stop my membership']:

  print('Q:', q)

  for score, doc in search(q, k=2):

      print(f'   {score}  {doc}')

  print()

#  EXPECTED OUTPUT

# Q: how do I get my money back?

#  0.62  Refunds are processed within 5-7 business days to the original card.

#  0.31  Download invoices from the Billing History section of your account.

 

# Q: when can I reach you?

#  0.55  Our support hours are 9am to 6pm IST, Monday to Friday.

#  0.18  ...

 

# Q: I want to stop my membership

#  0.60  To cancel, go to Settings > Subscription and choose Cancel Plan.

#   0.44  You can change your subscription plan under Settings > Billing.
