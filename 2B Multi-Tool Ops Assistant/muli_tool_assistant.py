import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Challenge 2B: The Multi-Tool Ops Assistant

# Challenge  •  ~35 minutes

# Problem Statement: Real questions need several tools. Build an assistant that can use a calculator, a date tool, and a project-owner directory, and keeps calling tools in a loop until it can answer.

 

# Goal of the Problem: Build a full tool-execution loop with routing across multiple tools — the mechanism behind every 'tool-using agent'.

 

# Step 1.  Define three tools (reusing calculate from 2A).

from datetime import date
import ast, operator as op

def calculate(expression: str) -> str:

   """Safely evaluate a basic arithmetic expression."""

   ops = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,

          ast.Div: op.truediv, ast.Pow: op.pow, ast.USub: op.neg}

   def ev(node):

       if isinstance(node, ast.Constant): return node.value

       if isinstance(node, ast.BinOp):

           return ops[type(node.op)](ev(node.left), ev(node.right))

       if isinstance(node, ast.UnaryOp):

           return ops[type(node.op)](ev(node.operand))

       raise ValueError("unsupported expression")

   return str(ev(ast.parse(expression, mode="eval").body))

 

 

DIRECTORY = {

   "data migration": "Priya Nair",

   "website relaunch": "Marco Silva",

   "mobile app": "Aisha Khan",

}

 

def today_date() -> str:

   """Return today's date in ISO format."""

   return date.today().isoformat()

 

def employee_lookup(project: str) -> str:

   """Return the owner of a project by its name."""

   return DIRECTORY.get(project.lower().strip(), "Unknown owner")

 

# Expected output

# (no output — tools defined)

 

# Step 2.  Register the tool schemas and a dispatch table mapping names to functions.

tool_schemas = [

 {"type": "function", "function": {"name": "calculate",

   "description": "Evaluate an arithmetic expression.",

   "parameters": {"type": "object",

     "properties": {"expression": {"type": "string"}},

     "required": ["expression"]}}},

 {"type": "function", "function": {"name": "today_date",

   "description": "Get today's date (ISO).",

   "parameters": {"type": "object", "properties": {}}}},

 {"type": "function", "function": {"name": "employee_lookup",

   "description": "Find the owner of a project by name.",

   "parameters": {"type": "object",

     "properties": {"project": {"type": "string"}},

     "required": ["project"]}}},

]

 

available = {"calculate": calculate,

            "today_date": today_date,

            "employee_lookup": employee_lookup}

 

# Expected output

# (no output — schemas & dispatch table ready)

 

# Step 3.  Write the agent loop: keep calling tools until the model stops requesting them.

import json

 

def run_agent(question, max_turns=5):

   messages = [

       {"role": "system", "content":

        "You are an operations assistant. Use tools when needed. "

        "Call one or more tools to get facts, then answer."},

       {"role": "user", "content": question}]

   for _ in range(max_turns):

       resp = client.chat.completions.create(

           model="gpt-4o-mini", messages=messages,

           tools=tool_schemas, tool_choice="auto")

       msg = resp.choices[0].message

       if not msg.tool_calls:

           return msg.content

       messages.append(msg)

       for call in msg.tool_calls:

           fn = available[call.function.name]

           args = json.loads(call.function.arguments or "{}")

           output = str(fn(**args))

           print(f"  [tool] {call.function.name}({args}) -> {output}")

           messages.append({"role": "tool",

                             "tool_call_id": call.id, "content": output})

   return "Stopped: max turns reached."

 

# Expected output

# (no output — agent loop defined)

 

# Step 4.  Ask one question that forces THREE different tools.

print(run_agent(

   "Who owns the data migration project, and what is 15% of a 240-hour "

   "effort estimate? Also tell me today's date."))

 

# Expected output

#  [tool] employee_lookup({'project': 'data migration'}) -> Priya Nair

#  [tool] calculate({'expression': '0.15*240'}) -> 36.0

#  [tool] today_date({}) -> 2026-07-28

# The data migration project is owned by Priya Nair. 15% of a 240-hour

# estimate is 36 hours. Today's date is 2026-07-28.