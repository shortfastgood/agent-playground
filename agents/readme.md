# AI Agents Prototypes

This section contains the prototypes of the AI agents developed in the project.

## Java Dependencies Update Agent

This agent is designed to update Java dependencies in Gradle and Maven projects. It intelligently parses the project files, identifies dependencies, and updates them to their latest stable versions. The agent supports both Azure OpenAI and Anthropic APIs for AI processing.

- [Java Dependencies Update Specification](java_dependecies_update_spec.md): This document outlines the requirements and specifications for the Java dependencies update agent.
- [Java Dependencies Update User Guide](java_dependencies_update_user_guide.md): This document provides a user guide for the Java dependencies update agent, including installation instructions, configuration, and usage examples.
- [Java Dependencies Update Code](java_dependencies_update.py): This is the implementation of the Java dependencies update agent. It includes the main logic for parsing and updating Gradle and Maven project files.
- [Java Dependencies Update Configuration](config.json): This is the configuration file used by the Java dependencies update agent. It contains settings for the AI provider and Maven repository.
