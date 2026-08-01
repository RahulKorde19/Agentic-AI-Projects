
import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Problem Statement: Before rolling out a customer-support summariser, finance wants an estimate: what will each call cost, and how does it change if we pick a cheaper or stronger model? You will build a small estimator.

# Goal of the Problem: Write a reusable function that, for any prompt and model, reports input tokens and estimated cost, then project a monthly bill and flag prompts that risk blowing a per-call budget.

# Where to run: VS Code (or Colab)

# Step 1 — Define pricing and the estimator

# Prices below are USD per 1,000,000 tokens (input, output). Check the current OpenAI pricing page for live numbers; the structure is what matters.

import tiktoken

 

enc = tiktoken.get_encoding("o200k_base")

 

# (input_price, output_price) in USD per 1,000,000 tokens

PRICING = {

   "gpt-4.1-nano": (0.10, 0.40),

   "gpt-4.1-mini": (0.40, 1.60),

   "gpt-4.1":      (2.00, 8.00),

}

 

def estimate(prompt, model, expected_output_tokens=300):

   in_tokens = len(enc.encode(prompt))

   in_price, out_price = PRICING[model]

   cost = (in_tokens / 1_000_000) * in_price \
    + (expected_output_tokens / 1_000_000) * out_price

   return in_tokens, cost

# Expected output

# no output yet — this cell only defines PRICING and estimate()

# Step 2 — Compare the three models on one prompt

prompt = "Summarise this customer's complaint and suggest a resolution. " * 40

 

print(f"{'model':14s} {'in_tokens':>9s} {'est_cost_usd':>13s}")

for model in PRICING:

   n, cost = estimate(prompt, model)

   print(f"{model:14s} {n:9d} {cost:13.6f}")

# Expected output

# model          in_tokens  est_cost_usd

# gpt-4.1-nano         440      0.000164

# gpt-4.1-mini         440      0.000656

# gpt-4.1              440      0.003280

# Same prompt, ~20x cost difference between nano and the full model. This is the model-selection lever in one table.

# Step 3 — Project a monthly bill

CALLS_PER_DAY = 5000

DAYS = 30

 

for model in PRICING:

   _, cost = estimate(prompt, model)

   monthly = cost * CALLS_PER_DAY * DAYS

   print(f"{model:14s} monthly ~ ${monthly:,.2f}")

# Expected output

# gpt-4.1-nano   monthly ~ $24.60

# gpt-4.1-mini   monthly ~ $98.40

# gpt-4.1        monthly ~ $492.00

# Step 4 — Add a per-call budget guardrail

BUDGET_PER_CALL = 0.001   # USD

 

def check_budget(prompt, model):

   _, cost = estimate(prompt, model)

   status = "OK" if cost <= BUDGET_PER_CALL else "OVER BUDGET"

   print(f"{model:14s} cost=${cost:.6f}  ->  {status}")

 

for model in PRICING:

  check_budget(prompt, model)

# Expected output

# gpt-4.1-nano   cost=$0.000164  -> OK

# gpt-4.1-mini   cost=$0.000656  -> OK

# gpt-4.1        cost=$0.003280  -> OVER BUDGET

 