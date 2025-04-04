# Agent-Playground
a playground to experiment with AI agents

This project is a laboratory whose purpose is to explore the world of artificial intelligence-based agents applied to software management and development.

To avoid yet another project without a final purpose, it is based on a concrete case that often troubles software production.

*In the Digital Banking section, we have a series of SLA contracts with customers for bug fixing. These contracts are attractive as long as the fixes remain inexpensive. A significant issue, however, is the verification of pull requests, which pile up and reduce the efficiency of senior team members, who are also the most highly paid. I've been asked if it might be possible to delegate an initial verification to artificial intelligence and, eventually, hand over trivial cases entirely to AI. This is an area where I've always needed some form of automation to evaluate the work of a junior developer. Ideally, it would merge with the original code, run the tests, and provide a report via email.*

The entire project is implemented using the "vibe coding" technique, which means delegating as much as possible to artificial intelligence. Both for development and for the actual use of what is produced, the goal is to limit additional costs and the use of additional resources compared to a project that doesn't make extensive use of artificial intelligence. The calculation therefore excludes all resources and costs that would be incurred anyway.

To start the project, an IDE (Intellij Ultimate) and a repository on the GitHub platform are used. Artificial intelligence is integrated using the GitHub-Copilot plugin in the paid version, which impacts costs in the order of 10 USD per month. Be aware: the indicated costs are for a small-scale implementation like this lab. An enterprise setup can cost up to four times as much. 

The texts, originally written in Italian, are translated and added to the documentation through Copilot Edits. The chosen model is Claude 3.7 Sonnet Thinking.

The additional tools and models used in this project are listed in [tools/installation.md](tools/installation.md).

## Prompts

A collection of prompts used to generate the documentation and the code are stored in the `prompts` directory.

## Architecture

Ideally, a large language model should be able to interface with the entire world using any language; obviously, this doesn't happen on its own. Currently, initiatives are continuously popping up here and there. One in particular seems to have certain consistency and a significant following: the Model Context Protocol (MCP), which aims to standardize agents' access to external resources.

That said, the implementation uses the latest version of Python and aims to be operational on MacOS, Windows (from version 11), and Linux (Ubuntu 24.04). As mentioned earlier, the project is hosted on the GitHub platform.

## Data Models

For a search or scan across different levels in the filesystem that leads to correct code analysis, a reflective model potentially large enough to function only with significant memory is required. Conversely, the results of these analyses can be divided into small steps to be executed in parallel. In the first case, we refer to Large Language Models (LLM), in the second case, Small Language Models (SLM).
