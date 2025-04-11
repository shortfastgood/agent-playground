# Java Dependencies Update Tool - User Guide

## Introduction

The Java Dependencies Update Tool is a command-line utility that automatically updates dependencies in Java projects to their latest stable versions. It supports both Gradle (build.gradle) and Maven (pom.xml) projects and leverages AI to intelligently parse and update dependency declarations.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation Steps

1. Clone the repository or download the source code.

2. Install the required dependencies:

   ```bash
   pip install -r agents/environment/requirements.txt
   ```

   This will install the following packages:
   - requests
   - openai (for Azure OpenAI support)
   - anthropic (for Anthropic Claude support)

3. Ensure the script is executable (Unix/Linux systems):

   ```bash
   chmod +x agents/environment/update_java_dependencies.py
   ```

## Configuration

### Environment Variables

Set one of the following environment variables depending on your chosen AI provider:

- For Azure OpenAI:
  ```bash
  export AZURE_API_KEY="your-azure-openai-api-key"
  ```

- For Anthropic:
  ```bash
  export ANTHROPIC_API_KEY="your-anthropic-api-key"
  ```

### Configuration File

The tool uses a configuration file (default: `config.json`) that defines parameters for the AI providers and Maven repository. 

Here's a sample configuration file:

```json
{
  "maven_central_url": "https://repo1.maven.org/maven2",
  "ai_provider": "azure",
  "azure_openai_endpoint": "https://your-azure-openai-endpoint.com/",
  "azure_openai_api_version": "2024-12-01-preview",
  "azure_openai_model": "gpt-4o",
  "anthropic_model": "claude-3-sonnet-20240229",
  "request_timeout": 60,
  "max_retries": 3
}
```

### Configuration Parameters

- `maven_central_url`: The base URL for Maven Central repository
- `ai_provider`: Default AI provider ("azure" or "anthropic")
- `azure_openai_endpoint`: Your Azure OpenAI endpoint URL
- `azure_openai_api_version`: API version for Azure OpenAI
- `azure_openai_model`: Model to use for Azure OpenAI
- `anthropic_model`: Model to use for Anthropic
- `request_timeout`: Timeout in seconds for API requests
- `max_retries`: Number of retries for failed API requests

## Usage

### Basic Syntax

```bash
python agents/environment/update_java_dependencies.py [file_path] [options]
```

#### Arguments

- `file_path`: Path to the build.gradle or pom.xml file to update

#### Options

- `--conf PATH`: Path to the configuration file (default: config.json)
- `--provider {azure,anthropic}`: AI provider to use (overrides configuration file)

### Examples

#### Update a Gradle project using default configuration

```bash
python agents/environment/update_java_dependencies.py path/to/build.gradle
```

#### Update a Maven project with a specific configuration file

```bash
python agents/environment/update_java_dependencies.py path/to/pom.xml --conf my_config.json
```

#### Update dependencies using a specific AI provider

```bash
python agents/environment/update_java_dependencies.py path/to/build.gradle --provider anthropic
```

## How It Works

1. The tool reads the specified Gradle or Maven file
2. It parses the file to extract all dependency declarations using AI
3. For each dependency, it queries Maven Central to find the latest stable version
4. It updates the file with the new dependency versions
5. The updated file is written back to disk

## Limitations

- The tool skips milestone (M) and release candidate (RC) versions
- It requires internet access to query the Maven Central repository
- Dependencies from repositories other than Maven Central may not be updated correctly
- Dependencies without explicit version numbers (common in Gradle projects using version catalogs or BOM dependencies) are identified but not updated

## Troubleshooting

### Common Issues

- **API Key Issues**: Ensure the appropriate environment variable is set based on your chosen provider
- **Configuration File Errors**: Verify that your configuration file is valid JSON and contains the required fields
- **Connection Errors**: Check your internet connection and verify the Maven Central URL is accessible
- **Parser Errors**: For complex build files, the AI parser might require refinements to the configuration

If you encounter any issues, check the log output for error messages, which will provide more information about the problem.
