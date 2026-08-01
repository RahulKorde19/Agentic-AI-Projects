import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# 3B: The Research Scout

# Problem Statement: Turn the single lookup into a 'scout' agent that researches a topic by making several external lookups and then synthesises a crisp stakeholder brief.
 
# Goal of the Problem: Combine external tools + a multi-turn loop + synthesis. This is the 'scout' agent pattern used for research assistants.

# Step 1.  Reuse wiki_summary from 3A, then build a loop that lets the agent search several times before writing.

import json

 

scout_tools = [{"type": "function", "function": {

   "name": "wiki_summary",

   "description": "Get a short factual summary of a topic from Wikipedia "

                  "(title with underscores).",

   "parameters": {"type": "object",

       "properties": {"title": {"type": "string"}},

       "required": ["title"]}}}]

 
import requests

 

def wiki_summary(title: str) -> str:

   """Fetch a short summary of a topic from Wikipedia."""

   url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"

   r = requests.get(url, timeout=10,

                     headers={"User-Agent": "agentic-workshop/1.0"})

   if r.status_code != 200:

       return f"No article found for '{title}'."

   return r.json().get("extract", "No summary available.")


def research_scout(request, max_turns=6):

   messages = [

       {"role": "system", "content":

        "You are a research scout. Gather facts using the wiki_summary tool "

        "(call it several times for different sub-topics), then produce a crisp "

        "5-bullet stakeholder brief. Ground every bullet in what you found."},

       {"role": "user", "content": request}]

   for _ in range(max_turns):

       resp = client.chat.completions.create(model="gpt-4o-mini",

                messages=messages, tools=scout_tools, tool_choice="auto")

       msg = resp.choices[0].message

       if not msg.tool_calls:

           return msg.content

       messages.append(msg)

       for call in msg.tool_calls:

           args = json.loads(call.function.arguments)

           print(f"  [scout searched] {args['title']}")

           messages.append({"role": "tool", "tool_call_id": call.id,

                            "content": wiki_summary(**args)})

   return "Max turns reached."

 

# Expected output

# (no output — scout defined)

 

# Step 2.  Ask for a brief. Watch the scout make multiple searches, then write.

print(research_scout(

   "Prepare a 5-bullet brief on the history and impact of large language "

   "models for a non-technical executive."))

 

# Expected output

 

#  [scout searched] Large_language_model

#  [scout searched] GPT-3

#  [scout searched] Transformer_(deep_learning_architecture)

# - LLMs are neural networks trained on huge text corpora...

# - The Transformer architecture (2017) made them scalable...

# - GPT-3 (2020) showed few-shot capabilities...

# - Impact spans search, coding, and customer support...

# - Key risks: hallucination, cost, and data governance.

# (searched titles and wording will vary)

 

 