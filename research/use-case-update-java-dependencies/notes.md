# Update Java Dependencies Agent

## Objective
The objective of this research is to develop a simple and useful AI and to test it using different providers and models. A secondary objective is to evaluate if the performance of a local provider on existing hardware is sufficient.

## Scope Boundaries
The scope of this research is limited to the use of AI for updating Java dependencies in Gradle and Maven projects.

## Key Question
Is a local provider sufficient for the task of updating Java dependencies in Gradle and Maven projects?

## Strategy
The development starts by writing a first version of the specification in natural language, ensuring clarity and precision. Development proceeds interactively with a collaboration between the developer and artificial intelligence. The files are modified, predominantly, by the AI agent chosen as the co-developer.

## AI Agent for Development

The chosen agent should be available as a native implementation on Linux, MacOS, and Windows. The agent must also allow the selection of different models, as this is a rapidly evolving field.

Another condition is that the chosen language model should support a certain number of natural languages without resulting in excessive penalties compared to English.

The agent that meets all the criteria, including automatic file updates, is GitHub Copilot with the Claude 3.7 Sonnet Thinking model in the plugin version (IntelliJ or Visual Studio Code).

From a development perspective, using the vibe coding technique, the preferred agent is Claude Coding, also with the Claude 3.7 Sonnet model. However, it is currently not available natively on Windows.
