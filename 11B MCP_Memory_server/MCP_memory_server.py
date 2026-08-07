# Exercise 8B  Build an MCP Memory Server (FastMCP)   

# Environment: VS Code (local, Python 3.10+ ; needs Node for the Inspector)    

# Problem Statement:  Build a local MCP server that exposes save_memory and search_memory tools backed by a vector store, then test it with the MCP Inspector so any MCP-compatible client can use it.

# Goal of the Problem:  Learn how memory is exposed to agents through the Model Context Protocol — the open standard behind shareable tools and memory.

 

# Step 1 —  Create the project and virtual environment

# Open a VS Code terminal and run:

# Terminal

# mkdir mcp-memory && cd mcp-memory

# python -m venv .venv

# Windows (PowerShell):  .venv\Scripts\Activate.ps1

# macOS / Linux:         source .venv/bin/activate

# pip install "mcp[cli]>=1.28,<2" openai numpy

 

# Expected output

# A virtual environment is created and the MCP SDK, OpenAI and numpy install.

# (Pinning <2 keeps the stable FastMCP import used below.)

 

# Step 2 —  Set your API key in this terminal

# Terminal

# # Windows (PowerShell):

# $env:OPENAI_API_KEY = "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"

# # macOS / Linux:

# export OPENAI_API_KEY="sk-...paste-your-key-here..."

 

# Expected output

# (No output. The key is now set for this terminal session.)

 

# Step 3 —  Create server.py

# Create a file named server.py and paste this. It's a complete MCP server.

# Python

from mcp.server.fastmcp import FastMCP

from openai import OpenAI

import numpy as np

 

mcp = FastMCP("memory-server")

client = OpenAI()

MEMORIES = []          # each item: (text, embedding)

 

def _embed(text):

  return client.embeddings.create(

      model="text-embedding-3-small", input=[text]).data[0].embedding

 

@mcp.tool()

def save_memory(text: str) -> str:

  """Save a piece of text to long-term memory."""

  MEMORIES.append((text, _embed(text)))

  return f"Saved. Total memories: {len(MEMORIES)}"

 

@mcp.tool()

def search_memory(query: str, k: int = 3) -> str:

  """Return the most relevant saved memories for a query."""

  if not MEMORIES:

       return "No memories yet."

  qv = np.array(_embed(query))

  def score(m):

       v = np.array(m[1])

       return float(np.dot(qv, v) / (np.linalg.norm(qv) * np.linalg.norm(v)))

  ranked = sorted(MEMORIES, key=score, reverse=True)[:k]

  return "\n".join(f"- {t}" for t, _ in ranked)

 

if __name__ == "__main__":

  mcp.run()

 

# Expected output

# (No output when saved. This file, server.py, is a complete MCP server that

# exposes two memory tools to ANY MCP-compatible client.)

 

# Step 4 —  Launch the MCP Inspector and test the tools

# Run this from the project folder (Node/npx required):

# Terminal

# npx @modelcontextprotocol/inspector python server.py

 

# Expected output

# The MCP Inspector opens in your browser. In the Tools tab you will see

# save_memory and search_memory. Call save_memory a few times (e.g. "Priya

# likes mango lassi", "The Premium plan is $20/month"), then call search_memory

# with "what does Priya drink?" and watch it return the ranked matching memory.

# Any MCP client (Claude Desktop, VS Code, an OpenAI agent) can now use this

# same memory server.

 