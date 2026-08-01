import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Code Based) 

# Quick Win 2A: Give the Agent a Calculator

# Quick Win  •  ~20 minutes

# Problem Statement: LLMs are unreliable at exact arithmetic. Let the model call a real Python function to compute the answer, instead of guessing.

 

# Goal of the Problem: Understand tool use / function calling: the model decides WHICH tool to call and with WHAT arguments; your code runs the tool and returns the result.

 

# Step 1.  Define the tool as an ordinary, safe Python function.

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

 

print(calculate("(1234*56)/7 + 89"))

 

# Expected output

# 9961.0

 

# Step 2.  Describe the tool to the model using the tools schema.

tools = [{

   "type": "function",

   "function": {

       "name": "calculate",

       "description": "Evaluate an arithmetic expression and return the result.",

       "parameters": {

           "type": "object",

           "properties": {

               "expression": {"type": "string",

                               "description": "A math expression, e.g. '2*(3+4)'"}

           },

           "required": ["expression"],

       },

   },

}]

 

# Expected output

# (no output — schema defined)

 

# Step 3.  Ask a question that needs the tool, and see the model REQUEST the call.

messages = [{"role": "user",

            "content": "What is 1234 times 56, divided by 7, plus 89?"}]

 

first = client.chat.completions.create(

   model="gpt-4o-mini", messages=messages, tools=tools, tool_choice="auto")

 

msg = first.choices[0].message

print(msg.tool_calls)

 

# Expected output

# [ChatCompletionMessageToolCall(id='call_...', function=Function(

#   arguments='{"expression":"1234*56/7+89"}', name='calculate'), 

#  type='function')]

 

# Step 4.  Run the requested tool and feed the result back for a final answer.

import json

 

messages.append(msg)                      # the assistant's tool-call message

for call in msg.tool_calls:

   args = json.loads(call.function.arguments)

   result = calculate(args["expression"])

   messages.append({"role": "tool",

                     "tool_call_id": call.id,

                    "content": result})

 

second = client.chat.completions.create(model="gpt-4o-mini", messages=messages)

print(second.choices[0].message.content)

 

# Expected output

 

# 1234 times 56, divided by 7, plus 89 equals 9961.

 