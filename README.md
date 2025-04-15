# Agent-Playground
a playground to experiment with AI agents

This project is a laboratory whose purpose is to explore the world of artificial intelligence-based agents applied to software management and development.

To avoid yet another project without a final purpose, it is based on a concrete case that often troubles software production.

*In the Digital Banking section, we have a series of SLA contracts with customers for bug fixing. These contracts are attractive as long as the fixes remain inexpensive. A significant issue, however, is the verification of pull requests, which pile up and reduce the efficiency of senior team members, who are also the most highly paid. I've been asked if it might be possible to delegate an initial verification to artificial intelligence and, eventually, hand over trivial cases entirely to AI. This is an area where I've always needed some form of automation to evaluate the work of a junior developer. Ideally, it would merge with the original code, run the tests, and provide a report via email.*

The project utilizes the "vibe coding" paradigm, which emphasizes maximum delegation to artificial intelligence systems throughout the development lifecycle. The strategic objective focuses on optimizing resource efficiency by minimizing supplementary costs when compared with conventional projects lacking significant AI integration. Consequently, the economic evaluation framework excludes baseline infrastructure and personnel allocations that would be requisite regardless of intelligent automation implementation.

To start the project, an IDE (Intellij Ultimate) and a repository on the GitHub platform are used. Artificial intelligence is integrated using the GitHub-Copilot plugin in the paid version, which impacts costs in the order of 10 USD per month. Be aware: the indicated costs are for a small-scale implementation like this lab. A business seat costs 19 USD per month by Amazon, Anthropic, and GitHub.

The texts, originally written in Italian, are translated and added to the documentation through Copilot Edits. The chosen model is Claude 3.7 Sonnet Thinking.

The additional tools and models used in this project are listed in [tools/installation.md](tools/installation.md).

## More Use Cases

The project is designed to be extensible and adaptable to various use cases. Here are some additional scenarios where the principles and tools developed in this project can be applied:

**Legacy Code Modernization**: 

A concrete uses case is the reverse engineering of an existing monolithic application into a microservices' architecture. 
This involves analyzing the existing codebase, identifying components that can be separated into microservices, 
and generating the necessary code and configuration files for the new architecture.

**Automated Testing**: 

Many organizations struggle with maintaining a comprehensive suite of automated tests. 
The coverage of the codebase is often low, and writing tests can be time-consuming.

**Image Analysis**:

A concrete uses case is the analysis of the widgets in a web/mobile application to reproduce the same behavior in a different context.

## AI Agents
- [Agents](agents/readme.md): This section contains the prototypes of the AI agents developed in the project.

## Strategy

The approach to provide a suitable implementation to an IT use case does not change with the introduction of artificial intelligence; a strategy is always necessary. First of all, it must be kept in mind that our digital assistant needs to be instructed correctly. The assistant has both technical and content limitations.

The amount of information we can provide to the model at once depends on the size of the installation; with a local installation, it's necessary to divide the work into tasks that are as simple as possible. 

The relevance of the responses depend on the model: if the topic concerns a software package with many new features released after our model's publication, we will likely not obtain relevant answers to our questions.

Additionally, artificial intelligence is not deterministic and often proves inconsistent and volatile; restricting its scope and steering it toward a stable path remains a task that must be carried out by human intelligence.

## Prompts

A collection of prompts used to generate the documentation and the code are stored in the `prompts` directory.
Be aware that the prompts doesn't guarantee the same results as the ones used in the project, 
the AI world is not deterministic and the results may vary depending on the context and the model used.

## Architecture

Ideally, a large language model should be able to interface with the entire world using any language; obviously, this doesn't happen on its own. Currently, initiatives are continuously popping up here and there. One in particular seems to have certain consistency and a significant following: the Model Context Protocol (MCP), which aims to standardize agents' access to external resources.

- [**Model Context Protocol**](mcp/mcp.md): The Model Context Protocol (MCP) is a protocol designed to facilitate the interaction between AI agents and their environment. It provides a structured way for agents to communicate, share information, and collaborate on tasks. The MCP is particularly useful in scenarios where multiple agents need to work together to achieve a common goal.

## Data Models

For a search or scan across different levels in the filesystem, that produces a correct code analysis, a large reflective model, potentially using a significant amount of memory, is required. Conversely, the results of these analyses can be divided into small steps to be executed in parallel. In the first case, we refer to Large Language Models (LLM), in the second case, Small Language Models (SLM).

For further details on the models used, see [research/models/models-research.md](research/models/models-research.md).

## Research

The research section is dedicated to the study of the models used in the project. The goal is to understand how they work and how to use them effectively. The research is divided into two main areas: Large Language Models (LLM) and Small Language Models (SLM). For further details, see [research/research.md](research/research.md).

