# Exercise 6B  Travel Crew with a Budget-Auditor Tool    DEEP DIVE

# Environment: Google Colab (Python + CrewAI)     Est. time: 22–25 min

# Problem Statement:  A CrewAI Planner proposes an itinerary; a Budget Auditor uses a custom Python tool to check the total against a hard limit and forces a revision if it's over budget.

# Goal of the Problem:  Combine multi-agent collaboration, custom tools and constraint validation in one workflow.

 

# Step 1 —  Install CrewAI and set your key

# Python

# !pip install crewai --quiet

import os

os.environ["OPENAI_API_KEY"] = "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"

os.environ["OPENAI_MODEL_NAME"] = "gpt-4o-mini"   # cheaper default (CrewAI uses gpt-4o otherwise)

 

# Expected output

# Installs CrewAI and its dependencies (takes ~1-2 minutes on first run).

 

# Step 2 —  Define a custom budget-checking tool

# Python

from crewai.tools import tool

 

@tool("budget_checker")

def budget_checker(total_cost: float, limit: float) -> str:

  """Check whether an itinerary total_cost is within the budget limit."""

  if total_cost <= limit:

       return f"WITHIN BUDGET: {total_cost} <= {limit}"

  return f"OVER BUDGET by {total_cost - limit}. The planner must cut costs and revise."

 

# Expected output

# (No output - a custom CrewAI tool. If the import fails, use:

# from crewai_tools import tool)

 

# Step 3 —  Define the Planner and the tool-using Auditor

# Python

from crewai import Agent, Task, Crew, Process

import os

os.environ["OPENAI_MODEL_NAME"] = "gpt-4o-mini"

 

planner = Agent(

  role="Travel Planner",

  goal="Create a {days}-day {dest} itinerary with per-item costs and a clear TOTAL",

  backstory="You design efficient, enjoyable trips.",

  verbose=True, allow_delegation=False)

 

auditor = Agent(

  role="Budget Auditor",

  goal="Ensure the itinerary total is within ${limit} using the budget_checker tool",

  backstory="You guard the budget and never approve an over-budget plan.",

  tools=[budget_checker], verbose=True, allow_delegation=False)

 

# Expected output

# (No output - a Planner and a tool-using Auditor.)

 

# Step 4 —  Wire the tasks and run

# Python

plan_task = Task(

  description="Plan a {days}-day trip to {dest}. List each item with a cost and a clear TOTAL in USD.",

  expected_output="An itinerary with a total cost", agent=planner)

 

audit_task = Task(

  description=("Use budget_checker on the itinerary total versus the ${limit} limit. "

                "If it is over budget, cut items and present a corrected within-budget itinerary."),

  expected_output="A within-budget final itinerary", agent=auditor, context=[plan_task])

 

crew = Crew(agents=[planner, auditor], tasks=[plan_task, audit_task],

           process=Process.sequential, verbose=True)

result = crew.kickoff(inputs={"dest": "Rome", "days": 3, "limit": 500})

print("\n===== FINAL =====\n")

print(result.raw)

 

# Expected output

# # Agent: Travel Planner  -> proposes a 3-day Rome itinerary, TOTAL: $560

# # Agent: Budget Auditor  -> Using tool budget_checker ...

# #  Tool result: OVER BUDGET by 60.0. The planner must cut costs and revise.

# # Agent: Budget Auditor  -> presents a trimmed itinerary, TOTAL: $480

 

# ===== FINAL =====