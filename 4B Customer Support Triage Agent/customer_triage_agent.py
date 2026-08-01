import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Challenge 4B: A Customer-Support Triage Agent

# Challenge  •  ~35 minutes

# Problem Statement: Build a support agent with two domain tools: it looks up an order, checks refund eligibility, and replies to the customer — chaining the tools automatically.

 

# Goal of the Problem: Give an agent real business tools and a role, then let it orchestrate a multi-step task end-to-end. This is how internal 'copilot' agents are built.

 

# Step 1.  Define two custom domain tools over a mock order database.

from langchain_core.tools import tool

 

ORDERS = {

   "A1001": {"item": "Wireless Mouse", "days_since_purchase": 10, "price": 25.0},

   "A1002": {"item": "Mechanical Keyboard", "days_since_purchase": 45, "price": 80.0},

}

 

@tool

def lookup_order(order_id: str) -> str:

   """Look up an order by ID: returns item, days since purchase, and price."""

   o = ORDERS.get(order_id.strip().upper())

   if not o:

       return "Order not found."

   return (f"{o['item']}, {o['days_since_purchase']} days since purchase, "

           f"price {o['price']} USD")

 

@tool

def refund_eligibility(days_since_purchase: int) -> str:

   """Check refund eligibility. Refunds are allowed within 30 days."""

   if days_since_purchase <= 30:

       return "Eligible for a full refund."

   return "Not eligible (past the 30-day window)."

 

# Expected output

# (no output — tools defined)

 

# Step 2.  Create the agent with a role via the prompt argument.

from langchain_openai import ChatOpenAI

from langgraph.prebuilt import create_react_agent

 

model = ChatOpenAI(model="gpt-4o-mini")

support_agent = create_react_agent(

   model,

   tools=[lookup_order, refund_eligibility],

   prompt=("You are a customer-support agent. First look up the order, then "

           "check refund eligibility using the days since purchase, then reply "

           "to the customer in 2-3 friendly sentences."))

 

# Expected output

# (no output — agent ready)

# Note: on older langgraph the argument is called 'state_modifier' instead of 'prompt'.

 

# Step 3.  Run two scenarios and watch the outcome differ automatically.

for oid in ["A1001", "A1002"]:

   r = support_agent.invoke({"messages": [("user",

       f"Hi, I would like a refund for order {oid}.")]})

   print(f"--- {oid} ---")

   print(r["messages"][-1].content, "\n")

 

# Expected output

 

# --- A1001 ---

# Good news! Your Wireless Mouse was purchased 10 days ago, so it is

# within our 30-day window and eligible for a full refund...

 

# --- A1002 ---

# Thanks for reaching out. Your Mechanical Keyboard was purchased 45

# days ago, which is past our 30-day refund window, so it is not

# eligible for a refun