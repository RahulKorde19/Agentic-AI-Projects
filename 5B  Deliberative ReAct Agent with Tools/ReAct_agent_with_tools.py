import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Exercise 1B  Deliberative ReAct Agent with Tools    DEEP DIVE

# Environment: Google Colab (Python + OpenAI)     Est. time: 15–20 min

# Problem Statement:  Build a deliberative agent that reasons in Thought → Action → Observation cycles and calls tools (a calculator and a mini knowledge base) to answer a multi-step question.

# Goal of the Problem:  Contrast deliberation with reaction, and learn the OpenAI tool-calling loop that powers most real agents.

 

# Step 1 —  Install the library and set your API key

# Run this once per session. Paste the OpenAI API key you were given.

# Python

# !pip install openai --quiet

 

# Python

import os

os.environ["OPENAI_API_KEY"] = "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"

 

# Expected output

# (No output. The key is now available to the OpenAI client.)

 

# Step 2 —  Define two tools

# Python

import json

 

def calculator(expression: str) -> str:

  try:

       return str(eval(expression, {"__builtins__": {}}, {}))

  except Exception as e:

       return f"error: {e}"

 

KB = {

  "founding_year_openai": "2015",

  "ceo_openai": "Sam Altman",

  "speed_of_light_km_s": "299792",

}

 

def knowledge_lookup(key: str) -> str:

  return KB.get(key, "not found")

 

# Expected output

# (No output - defines two tools the agent can call.)

 

# Step 3 —  Describe the tools to the model

# Python

tools = [

{"type": "function", "function": {

    "name": "calculator",

    "description": "Evaluate a math expression, e.g. '23*7+5'.",

    "parameters": {"type": "object",

       "properties": {"expression": {"type": "string"}}, "required": ["expression"]}}},

{"type": "function", "function": {

    "name": "knowledge_lookup",

    "description": "Look up a fact by key. Keys: founding_year_openai, ceo_openai, speed_of_light_km_s.",

    "parameters": {"type": "object",

       "properties": {"key": {"type": "string"}}, "required": ["key"]}}},

]

available = {"calculator": calculator, "knowledge_lookup": knowledge_lookup}

 

# Expected output

# (No output - this is the tool "menu" the model reads.)

 

# Step 4 —  Write the ReAct loop

# Python

from openai import OpenAI

client = OpenAI()

 

def deliberative_agent(question, max_steps=5):

  messages = [

     {"role": "system", "content": "You are a deliberative agent. Think step by step and use tools when needed."},

     {"role": "user", "content": question},

  ]

  for _ in range(max_steps):

       resp = client.chat.completions.create(

           model="gpt-4o-mini", messages=messages, tools=tools, tool_choice="auto")

       msg = resp.choices[0].message

       if not msg.tool_calls:                 # no tool needed -> final answer

           return msg.content

       messages.append(msg)

       for tc in msg.tool_calls:              # run each requested tool

           args = json.loads(tc.function.arguments)

           result = available[tc.function.name](**args)

           print(f"  [tool] {tc.function.name}({args}) -> {result}")

           messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})

  return "Stopped: max steps reached."

 

# Expected output

# (No output - defines the Thought -> Action -> Observation loop.)

 

# Step 5 —  Run a multi-step question

# Python

print(deliberative_agent(

  "What year was OpenAI founded, and what is that year multiplied by 2?"))

 

# Expected output

# [tool] knowledge_lookup({'key': 'founding_year_openai'}) -> 2015

# [tool] calculator({'expression': '2015*2'}) -> 4030

# OpenAI was founded in 2015, and that year multiplied by 2 is 4030.

# # The agent CHOSE which tools to use and in what order - that is deliberation.