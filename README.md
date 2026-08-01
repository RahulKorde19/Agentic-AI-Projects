# Agentic AI Projects

A structured portfolio of hands-on AI engineering exercises covering agent orchestration, tool use, retrieval systems, memory, and workflow automation. This repository is designed to showcase practical implementation of modern LLM application patterns with a strong focus on interoperability, experimentation, and production-minded design.

## Overview

This workspace demonstrates how to build:

- LLM-powered agents with memory and tool access
- Retrieval-augmented generation (RAG) pipelines
- Vector search and semantic retrieval workflows
- Structured output and tool-calling interfaces
- Multi-agent coordination using CrewAI
- MCP-based local tool servers for standardized model interaction

## Featured Projects

### 1. MCP Memory Server

A local Model Context Protocol (MCP) server exposing `save_memory` and `search_memory` tools backed by embeddings. The project illustrates how external memory can be surfaced to AI clients in a standardized, reusable way.

![MCP Inspector server view](Result%20Images/Screenshot%202026-08-01%20144747.png)

This screenshot highlights the MCP Inspector environment used to validate and test the server interface.

### 2. CrewAI Multi-Agent Workflow

A CrewAI-driven workflow for planning, execution, and validation tasks. The project shows how autonomous agents can collaborate on a goal, share context, and produce structured outputs such as itineraries and budget checks.

![CrewAI execution flow](Result%20Images/Screenshot%202026-08-01%20142619.png)

This screenshot demonstrates the task/agent execution traces used to orchestrate a multi-step reasoning workflow.

### 3. RAG + Chroma Vector Memory

A retrieval pipeline that stores and retrieves document context with vector similarity search using Chroma. This demonstrates how long-term memory and grounding can be added to an agent workflow.

![RAG retrieval example](Result%20Images/Screenshot%202026-08-01%20112345.png)

## Concepts Covered

- Prompt engineering and structured prompting
- OpenAI-compatible API usage
- Embedding generation and semantic similarity search
- RAG memory patterns
- MCP server implementation and local inspection
- CrewAI multi-agent collaboration
- Workflow orchestration, planning, and evaluation
- Tool calling and function-based agent design

## Project Areas

The repository includes exercises and mini-projects across the following themes:

- Tokenizer exploration
- Context window cost estimation
- Parameter comparison and temperature control
- Streaming and resilient chat
- Structured outputs and tool calling
- Chain-of-thought output contracts
- Guardrails and evaluation harnesses
- Geometry, semantic search, and keyword search
- RAG and memory systems
- Agentic task planning and external tool integration

## Tech Stack

- Python
- OpenAI SDK
- NumPy
- Chroma
- CrewAI
- Model Context Protocol (MCP)
- FastMCP

## Setup

1. Create and activate a Python virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Add your API key in a local environment or shell session.

4. Run the relevant project scripts from their folders.

## Notes

Some examples rely on API access from OpenAI or compatible providers. Secrets should stay local and must not be committed to GitHub.

## Portfolio Summary

These projects illustrate hands-on capability across agent architecture, retrieval, memory, and orchestration patterns. The work is well-suited for demonstrating practical implementation skills in AI application development, especially for roles involving agents, tools, search, and LLM systems design.
