import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Hands-on 2-A  - Fixed vs recursive chunking

# Problem Statement: A long document has to be broken into pieces before it can be embedded. Naive character-splitting cuts sentences in half. Compare naive splitting with recursive splitting that respects natural boundaries and adds overlap.

# Goal of the Problem: Understand chunk size, overlap, and boundary-awareness — and see why RecursiveCharacterTextSplitter is the sensible default.

# Step 1. Install the splitter library

#  CODE — copy & paste

# !pip install -q langchain-text-splitters

#  EXPECTED OUTPUT

# (installs quietly, no error)

# Step 2. Create a sample document

#  CODE — copy & paste

text = (

  'Retrieval-Augmented Generation grounds a language model in your own data. '

  'First, documents are split into chunks and embedded into vectors. '

   'The vectors are stored in a vector database for fast similarity search. '

   'At query time, the most relevant chunks are retrieved. '

   'Those chunks are added to the prompt so the model answers from facts, '

   'not from memory. This reduces hallucination and keeps answers current.'

)

print('Characters:', len(text))

#  EXPECTED OUTPUT

# Characters: 415

# Step 3. Split naively by character count

#  CODE — copy & paste

from langchain_text_splitters import CharacterTextSplitter

naive = CharacterTextSplitter(separator='', chunk_size=120, chunk_overlap=0)

chunks = naive.split_text(text)

print('Chunks:', len(chunks))

print('First chunk:', repr(chunks[0]))

#  EXPECTED OUTPUT

# Chunks: 4

# First chunk: 'Retrieval-Augmented Generation grounds a language model in your own data. First, documents are split into chunks an'

# (notice the word 'and' is cut off mid-sentence)

# Step 4. Split recursively with overlap

#  CODE — copy & paste

from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=120, chunk_overlap=30)

chunks = splitter.split_text(text)

print('Chunks:', len(chunks))

for i, ch in enumerate(chunks):

   print(f'[{i}] ({len(ch)} chars) {ch}')

#  EXPECTED OUTPUT

# Chunks: 5

# [0] (118 chars) Retrieval-Augmented Generation grounds a language model in your own data.

# [1] (115 chars) First, documents are split into chunks and embedded into vectors.

# ... (chunks break on sentence/word boundaries, with a little overlap carried forward)

# 💡 The recursive splitter tries paragraph, then sentence, then word boundaries before it ever cuts mid-word. The 30-char overlap keeps context from leaking across the boundary — a common fix when answers 'fall between' two chunks.