
import os

from dotenv import load_dotenv

from openai import OpenAI



load_dotenv()                     # reads .env into environment variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



# Exercise 2B  CrewAI Content Crew (Strategist + Writer + SEO Editor)    DEEP DIVE

 

# Problem Statement:  Build a three-agent CrewAI crew that turns a topic into a polished, SEO-ready article, with each agent's output feeding the next.

# Goal of the Problem:  Learn CrewAI's Agent / Task / Crew model, roles-goals-backstories, the sequential process, and automatic context passing.

 

# Step 1 —  Install CrewAI and set your key

# First run takes a minute or two. We pin gpt-4o-mini to keep it cheap.

# Python

# pip install crewai --quiet

import os

os.environ["OPENAI_API_KEY"] = "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"

os.environ["OPENAI_MODEL_NAME"] = "gpt-4o-mini"   # cheaper default (CrewAI uses gpt-4o otherwise)

 

# Expected output

# Installs CrewAI and its dependencies (takes ~1-2 minutes on first run).

 

# Step 2 —  Define three specialised agents

# Python

from crewai import Agent, Task, Crew, Process

 

strategist = Agent(

  role="Content Strategist",

  goal="Produce 5 sharp talking points on {topic}",

  backstory="You distill complex topics into crisp angles for busy professionals.",

  verbose=True, allow_delegation=False)

 

writer = Agent(

  role="Writer",

  goal="Write a clear ~200-word article on {topic}",

  backstory="You turn talking points into engaging, readable prose.",

  verbose=True, allow_delegation=False)

 

editor = Agent(

  role="SEO Editor",

  goal="Polish the article and add a compelling title plus 3 keywords",

  backstory="You sharpen writing and make it easy to discover.",

  verbose=True, allow_delegation=False)

 

# Expected output

# (No output - three specialised agents are now defined.)

 

# Step 3 —  Define the tasks (note the context chaining)

# Python

t1 = Task(description="List 5 talking points on {topic}.",

         expected_output="5 concise bullet points", agent=strategist)

 

t2 = Task(description="Write a ~200-word article on {topic} using the talking points.",

         expected_output="A ~200-word article", agent=writer, context=[t1])

 

t3 = Task(description="Edit the article. Add an SEO-friendly title and 3 keywords.",

         expected_output="Final article with a title and 3 keywords", agent=editor, context=[t2])

 

# Expected output

# (No output. Note context=[t1] and context=[t2]: each task automatically

# receives the previous task's output as input.)

 

# Step 4 —  Assemble the crew and run

# Python

crew = Crew(agents=[strategist, writer, editor],

           tasks=[t1, t2, t3],

           process=Process.sequential, verbose=True)

 

result = crew.kickoff(inputs={"topic": "AI agents for financial analysts"})

print("\n===== FINAL =====\n")

print(result.raw)

 

# Expected output

# Agent: Content Strategist

## Task: List 5 talking points ...

# Agent: Writer

## Task: Write a ~200-word article ...

# Agent: SEO Editor

## Task: Edit the article ...

 

# ===== FINAL =====