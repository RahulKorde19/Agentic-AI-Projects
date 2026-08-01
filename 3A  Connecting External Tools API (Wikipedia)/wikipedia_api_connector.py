
import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Set 3 — Connecting Real External Tools (via APIs)

# Quick Win 3A: Plug in a Real Web Tool (Wikipedia)

# Quick Win  • ~20 minutes

# Problem Statement: Give the agent access to live external knowledge by wiring up a real public API (Wikipedia) as a tool it can call.

 

# Goal of the Problem: Learn tool abstraction: any API can become an agent tool. Here the agent fetches fresh facts instead of relying only on its training data.

 

# Step 1.  Build the external tool with a plain HTTP request (no API key needed).

import requests

 

def wiki_summary(title: str) -> str:

   """Fetch a short summary of a topic from Wikipedia."""

   url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"

   r = requests.get(url, timeout=10,

                     headers={"User-Agent": "agentic-workshop/1.0"})

   if r.status_code != 200:

       return f"No article found for '{title}'."

   return r.json().get("extract", "No summary available.")

 

print(wiki_summary("Reinforcement_learning")[:200])

 

# Expected output

# Reinforcement learning (RL) is an interdisciplinary area of machine learning and optimal control concerned with how an intelligent agent should take actions in a dynamic environment... (first 200 chars)

 

# Step 2.  Expose the tool to the model and run a one-shot tool call.

import json

 

tools = [{"type": "function", "function": {

   "name": "wiki_summary",

   "description": "Get a short factual summary of a topic from Wikipedia. "

                  "Use the article title with underscores.",

   "parameters": {"type": "object",

       "properties": {"title": {"type": "string"}},

       "required": ["title"]}}}]

 

def answer_with_wiki(question):

   messages = [{"role": "user", "content": question}]

   resp = client.chat.completions.create(model="gpt-4o-mini",

            messages=messages, tools=tools, tool_choice="auto")

   msg = resp.choices[0].message

   if not msg.tool_calls:

       return msg.content

   messages.append(msg)

   for call in msg.tool_calls:

       args = json.loads(call.function.arguments)

       messages.append({"role": "tool", "tool_call_id": call.id,

                        "content": wiki_summary(**args)})

   final = client.chat.completions.create(model="gpt-4o-mini", messages=messages)

   return final.choices[0].message.content

 

print(answer_with_wiki(

   "In two sentences, explain 'Reinforcement learning'. Use Wikipedia."))

 

# Expected output

 

# A two-sentence, accurate explanation grounded in the fetched Wikipedia

# summary (mentions an agent learning by trial and error to maximise reward).

 