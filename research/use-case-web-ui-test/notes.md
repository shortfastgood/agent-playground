# Use Case Web UI Test

## Objective
The objective of this research is to develop a simple and useful AI agent and to test it with two different MCP servers. 
A secondary objective is to evaluate if the performance of a local provider on existing hardware is sufficient.

## Scope Boundaries
The purpose of this research is limited to evaluating the advantages of a user interface test compared to traditional record-and-playback or even coded tests.

## Key Question
Is the management of these tests throughout the lifecycle of this user interface less demanding with the use of artificial intelligence?

## Strategy
The development starts by writing a first version of the specification in natural language, ensuring clarity and precision. Development proceeds interactively with a collaboration between the developer and artificial intelligence. The files are modified, predominantly, by the AI agent chosen as the co-developer.

## AI Agent for Development

The chosen agent should be available as a native implementation on Linux, MacOS, and Windows. The agent must also allow the selection of different models, as this is a rapidly evolving field.

Another condition is that the chosen language model should support a certain number of natural languages without resulting in excessive penalties compared to English.

The agent that meets all the criteria, including automatic file updates, is GitHub Copilot with the Claude 3.7 Sonnet Thinking model in the plugin version (IntelliJ or Visual Studio Code).

From a development perspective, using the vibe coding technique, the preferred agent is Claude Coding, also with the Claude 3.7 Sonnet model. However, it is currently not available natively on Windows.
