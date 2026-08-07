# Step 3 —  Create server.py

# Create a file named server.py and paste this. It's a complete MCP server.

# Python



import os

from mcp.server.fastmcp import FastMCP

from openai import OpenAI

import numpy as np

 

mcp = FastMCP("memory-server")



client = OpenAI()

# client = OpenAI(api_key=os.getenv('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'"))


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
