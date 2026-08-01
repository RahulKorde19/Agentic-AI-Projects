import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
 

# Quick Win 4A: The Same Agent, 5 Lines with a Framework

 

# Problem Statement: Rebuild the calculator agent — but let a framework handle the whole tool loop for you.

 

# Goal of the Problem: See how much boilerplate a framework removes. create_react_agent runs the reason → act → observe loop automatically.

 

# Step 1.  Install the framework packages.

# !pip install -U langgraph langchain-openai (Google Collab)

# pip install -U langgraph langchain-openai (VS Code)

 

# Expected output

# Successfully installed langgraph-... langchain-openai-... (and deps)

 

# Step 2.  Define a tool with the @tool decorator and create the agent.

from langchain_openai import ChatOpenAI

from langchain_core.tools import tool

from langgraph.prebuilt import create_react_agent

 

@tool

def calculate(expression: str) -> str:

   """Evaluate a basic arithmetic expression like '2*(3+4)'."""

   import ast, operator as o

   ops = {ast.Add: o.add, ast.Sub: o.sub, ast.Mult: o.mul,

          ast.Div: o.truediv, ast.Pow: o.pow, ast.USub: o.neg}

   def ev(n):

       if isinstance(n, ast.Constant): return n.value

       if isinstance(n, ast.BinOp): return ops[type(n.op)](ev(n.left), ev(n.right))

       if isinstance(n, ast.UnaryOp): return ops[type(n.op)](ev(n.operand))

       raise ValueError("bad")

   return str(ev(ast.parse(expression, mode="eval").body))

 

model = ChatOpenAI(model="gpt-4o-mini")

agent = create_react_agent(model, tools=[calculate])

 

# Expected output

# (no output — agent ready)

 

# Step 3.  Invoke the agent. The tool loop runs for you.

result = agent.invoke({"messages": [("user",

   "What is 4567 times 12, minus 89? Then tell me if the result is even or odd.")]})

print(result["messages"][-1].content)

 

# Expected output

# 4567 x 12 - 89 = 54715, which is an odd number.

 

# Step 4.  Peek inside the loop to see the reasoning + tool call the framework ran.

for m in result["messages"]:

   m.pretty_print()

 

# Expected output

 

# ================ Human Message =================

# What is 4567 times 12, minus 89? ...

# ================= Ai Message ===================

# Tool Calls: calculate  ({'expression': '4567*12-89'})

# ================= Tool Message =================

# 54715

# ================= Ai Message ===================

# 54715, which is an odd number.

 

 
