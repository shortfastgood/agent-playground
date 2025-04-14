# Java Dependencies Update Specification

## Requirements
- Command line agent that updates Java dependencies in a Gradle or Maven project.
- The agent requires a single argument: the path of the file to be updated.
- If the file is a Gradle file, the agent should update the dependencies in the `build.gradle` file.
- If the file is a Maven file, the agent should update the dependencies in the `pom.xml` file.
- The agent should be able to update the version of a specific dependency to the latest version.
- The agent should support Azure OpenAI, Anthropic, and Ollama APIs. For Azure and Anthropic, the API key should be passed through environment variable. All other information should be passed through the configuration file.
- The AI provider can be specified using the `--provider` command-line argument with values `azure`, `anthropic`, or `ollama`. If not provided, it will use the provider specified in the configuration file.
- If no provider is defined either through command-line or configuration file, the agent should exit with an error.
- The configuration file path can be specified using the `--conf` argument. If not provided, it defaults to `config.json`.
- The agent should skip milestone (M), release candidate (RC), and alpha versions and use the highest stable version available. The detection of milestone, RC, and alpha versions should be case-insensitive (e.g., both "M1" and "m1", "RC2" and "rc2", "alpha1" and "ALPHA1" should be recognized).
- The agent should ignore or skip dependencies that don't have explicit version information (common in Gradle files where versions might be specified elsewhere, such as in version catalogs or BOM dependencies).

## Components
- Program file
- Configuration file: config.json (default) or specified via `--conf` argument

## Process
1. Read the file specified in the argument.
2. Determine if the file is a Gradle or Maven file.
3. If it is a Gradle file, parse the `build.gradle` file and get the dependencies, if it is a Maven file, parse the `pom.xml` file and get the dependencies, otherwise exit en inform the caller that the file is not a Gradle or Maven file.
4. The parsing should be done with a call to the AI chat. The AI chat should be able to parse the file and extract all dependency declarations regardless of format (implementation, compile, api, testImplementation for Gradle; dependencies section contents in Maven). Each dependency should be returned in a structured format with groupId, artifactId, and version. For dependencies without explicit versions, the version should be set to null or omitted.
5. For each dependency with a version, call the maven central repository API to get the latest version of the dependency.
6. The base URL for the maven central repository API is located in the configuration file.
7. The first part of the path is the base URL, and the second part is the group ID and artifact ID of the dependency.
8. If the group ID contains a dot, replace the dot with a slash.
9. The name of the file to get is maven-metadata.xml. Parse metadata.xml and get the latest version of the dependency. If the latest version ends with M<integer>, RC<integer>, or alpha<integer>, find the highest stable version instead.
10. Update the version of the dependency in the list build in step 4.
11. If the file is a Gradle file, update the `build.gradle` file with the new dependencies, if it is a Maven file, update the `pom.xml` file with the new dependencies.
12. The update should be done with a call to the AI chat. The AI chat should be able to update the file and return the updated file.
13. Write the updated file to the disk.

## Coding
- The code should be written in Python.
- The code should be modular and easy to read.
- The code should be well-documented.
- The code should be tested with a sample Gradle and Maven file.
- The code should be able to handle errors and exceptions.
- The main file is `agents/environment/update_java_dependencies.py`.
- The configuration file is `agents/environment/config.json` by default or can be specified with the `--conf` argument.
- The python requirements are in `agents/environment/requirements.txt`.

