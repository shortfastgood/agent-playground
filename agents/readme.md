# AI Agents Prototypes

This section contains the prototypes of the AI agents developed in the project.

## Java Dependencies Update Agent

This agent is designed to update Java dependencies in Gradle and Maven projects. It intelligently parses the project files, identifies dependencies, and updates them to their latest stable versions. The agent supports both Azure OpenAI and Anthropic APIs for AI processing.

- [**Notes**](../research/use-case-update-java-dependencies/notes.md): This document outlines the objectives, scope, key questions, and strategy for the Java dependencies update agent.
- [**Specification**](../research/use-case-update-java-dependencies/specifications): This document outlines the requirements and specifications for the Java dependencies update agent.
- [**User Guide**](../research/use-case-update-java-dependencies/user_guide): This document provides a user guide for the Java dependencies update agent, including installation instructions, configuration, and usage examples.
- [**Code**](../research/use-case-update-java-dependencies/sources/update_java_dependencies.py): This is the implementation of the Java dependencies update agent. It includes the main logic for parsing and updating Gradle and Maven project files.
- [**Configuration**](../research/use-case-update-java-dependencies/sources/config.json): This is the configuration file used by the Java dependencies update agent. It contains settings for the AI provider and Maven repository.
- [**Report**](../research/use-case-update-java-dependencies/report.md): This document provides a report on the performance and results of the Java dependencies update agent, including any limitations and future improvements.
