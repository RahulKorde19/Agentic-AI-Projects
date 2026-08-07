# Agentic AI Projects

A hands-on portfolio of agentic AI engineering work focused on building, evaluating, and integrating LLM-powered systems. This repository demonstrates practical experience across prompt design, tool calling, retrieval, memory, orchestration, and multi-agent workflows.

## Summary

This project collection showcases the ability to move from single-prompt experimentation to real agentic system design. It reflects work with:

- LLM application architecture
- Agent memory and context management
- Embedding-based retrieval and vector search
- Tool-calling and external function integration
- Multi-agent coordination using CrewAI
- Multi-agent orchestration with guarded, self-checking workflow design
- Standardized MCP server tooling for local AI workflows

The codebase is not just a set of notebooks or demos; it represents a progression of learning from foundational prompting patterns to more advanced agentic systems that emphasize interoperability, traceability, and practical use of LLMs in software workflows.

## What This Repository Demonstrates

This repository shows a strong working understanding of the following AI engineering concepts:

- Prompt and response design for deterministic, structured outputs
- Agent memory patterns for short-term and long-term context retention
- Retrieval-augmented generation (RAG) implementation
- Semantic and keyword search behavior
- Embedding-driven vector retrieval with ChromaDB
- Chunking strategies and retrieval quality comparison
- MCP server design for exposing reusable AI tools
- Multi-agent task decomposition and collaboration using CrewAI
- Multi-agent orchestration with guardrail-based self-verification
- End-to-end execution traces for real workflow visibility

## Featured Work

### 6. Treasury Liquidity & Intraday Cash Management Agent (Capstone)

This capstone project applies multi-agent orchestration to a treasury use case, with five specialized agents for aggregation, forecasting, funding recommendation, alerting, and governance commentary coordinated by a central orchestrator to monitor synthetic intraday cash positions and produce a governance-ready liquidity report.

![Treasury, Liquidity, and Intraday Cash Management Day](CAPSTONE- Treasury, Liquidity & Intraday Cash Management Agent/Treasury_Liquidity_and_Intraday_Cash_mgmpy_ppt.pdf)

![Treasury agent live demo](CAPSTONE-%20Treasury,%20Liquidity%20&%20Intraday%20Cash%20Management%20Agent/images%20for%20pdf/Screenshot%202026-08-06%20114810.png)

![Treasury agent backend decisions](CAPSTONE-%20Treasury,%20Liquidity%20&%20Intraday%20Cash%20Management%20Agent/images%20for%20pdf/Screenshot%202026-08-06%20114821.png)

This work highlights a full multi-agent pipeline with a central orchestrator, tool-calling with grounded and constrained outputs, a self-verifying guardrail agent that checks its own generated text against source data before display, graceful degradation design through per-agent fallback logic, and a fully spec-driven build process from PRD through acceptance criteria to source code. See the [full project README](CAPSTONE-%20Treasury,%20Liquidity%20&%20Intraday%20Cash%20Management%20Agent/README.md) for the complete architecture write-up, presentation deck, and live demo walkthrough.

### 1. MCP Memory Server

This project implements a lightweight local memory server using the Model Context Protocol (MCP). The server exposes memory tools that can be consumed by external MCP-compatible clients, demonstrating how tools and persistent context can be standardized and reused across systems.

![MCP Inspector server view](Result%20Images/Screenshot%202026-08-01%20144737.png)

This work highlights practical experience with tool-server integration, local agent interoperability, and a clean MCP-style interface.

### 2. CrewAI Multi-Agent Workflow

This project explores a coordinated multi-agent system where separate roles collaborate to complete a task end to end. The workflow demonstrates delegation, progress tracking, and structured output generation in a way that mirrors real production agent orchestration patterns.

![CrewAI execution flow](Result%20Images/Screenshot%202026-08-01%20123419.png)

![Agentic AI workflow trace](Result%20Images/Screenshot%202026-08-01%20112614.png)

![Agent orchestration output](Result%20Images/Screenshot%202026-08-01%20112654.png)

These visuals show the task execution flow, agent coordination, and the final generated result, which is especially relevant for demonstrating orchestration and workflow design capability.

### 3. ChromaDB Vector Store and Retrieval Workflow

This section focuses on semantic retrieval using embeddings and vector stores. It demonstrates how relevant context can be stored, retrieved, and used to ground an agent’s response in a more reliable way.

![ChromaDB query flow](Result%20Images/Screenshot%202026-07-28%20105028.png)

![Vector store retrieval view](Result%20Images/Screenshot%202026-08-01%20142619.png)

This is strong evidence of understanding retrieval architecture, memory grounding, and practical RAG design.

### 4. Chunking and Retrieval Quality Experiments

The repository also includes experimentation around fixed, recursive, and semantic chunking strategies. These exercises show a practical understanding of how chunk layout affects retrieval quality and downstream agent performance.

![Semantic vs fixed chunking](Result%20Images/Screenshot%202026-07-28%20104508.png)

### 5. Short-Term and Long-Term Memory Patterns

A key part of the learning journey in this repository is understanding agent memory design. This section demonstrates how context can be retained temporarily for conversational continuity and also stored for longer-term retrieval and reuse.

![Short-term and long-term memory](Result%20Images/Screenshot%202026-08-01%20144236.png)

### 6. Treasury Liquidity & Intraday Cash Management Agent (Capstone)

This capstone project applies multi-agent orchestration to a treasury use case, with five specialized agents for aggregation, forecasting, funding recommendation, alerting, and governance commentary coordinated by a central orchestrator to monitor synthetic intraday cash positions and produce a governance-ready liquidity report.

![Treasury agent live demo](CAPSTONE-%20Treasury,%20Liquidity%20&%20Intraday%20Cash%20Management%20Agent/images%20for%20pdf/Screenshot%202026-08-06%20114810.png)

![Treasury agent backend decisions](CAPSTONE-%20Treasury,%20Liquidity%20&%20Intraday%20Cash%20Management%20Agent/images%20for%20pdf/Screenshot%202026-08-06%20114821.png)

This work highlights a full multi-agent pipeline with a central orchestrator, tool-calling with grounded and constrained outputs, a self-verifying guardrail agent that checks its own generated text against source data before display, graceful degradation design through per-agent fallback logic, and a fully spec-driven build process from PRD through acceptance criteria to source code. See the [full project README](CAPSTONE-%20Treasury,%20Liquidity%20&%20Intraday%20Cash%20Management%20Agent/README.md) for the complete architecture write-up, presentation deck, and live demo walkthrough.

## What I Learned

Across this codebase, the most valuable takeaways are:

- How to build AI systems that go beyond a single prompt and become structured workflows
- How agents use tools, memory, and retrieval to improve task performance
- How RAG systems combine retrieval quality with grounded generation
- How MCP creates a reusable layer for AI tools and memory interfaces
- How orchestration frameworks like CrewAI help coordinate multi-step reasoning tasks
- Why chunking strategy, retrieval quality, and memory design matter for production-ready LLM applications

## Skills Developed

- Python development for AI applications
- OpenAI-compatible API integration
- Embedding and vector database workflows
- Agentic system design
- RAG and semantic search implementation
- MCP and tool-server integration
- Multi-agent coordination and workflow design
- Practical evaluation and debugging of LLM system behavior

## Project Areas Covered

- Tokenizer exploration
- Context window cost estimation
- Parameter comparison and temperature control
- Streaming and resilient chat
- Structured outputs and tool calling
- Chain-of-thought output contracts
- Guardrails and evaluation harnesses
- Treasury/liquidity agentic workflows
- Geometry, semantic search, and keyword search
- RAG and memory systems
- Agentic task planning and external tool integration

## Tech Stack

- Python
- OpenAI SDK
- NumPy
- ChromaDB
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

## Portfolio Closing Statement

This repository reflects a practical, applied learning path in modern AI engineering. The work spans foundational LLM usage through advanced agentic architectures, and it highlights the ability to design, implement, and reason about systems that combine prompting, memory, search, tools, and orchestration into coherent AI workflows.
