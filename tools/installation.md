# Installation Guide

This document outlines the steps to set up your development environment for the Agent Playground project. 

Unlike traditional detailed descriptions, this document only contains information specific to the project and its configurations. The tools used are well documented by their respective creators. For those who prefer not to read lengthy documentation, we suggest using AI chat capabilities. This approach is also one of the project's objectives, as it allows you to evaluate the benefits of interacting with your development tools.

## Prerequisites

Ensure you have the following installed on your system:

- Python 3.12+
- Git
- A text editor or IDE (Intellij Ultimate recommended, as used in the project)
- GitHub account with GitHub Copilot subscription (for AI-assisted development)
- [Ollama](https://ollama.com) LLM runner (for local model inference)
- [Aider Chat](https://aider.chat) (for local model inference)

## Supported Operating Systems

- MacOS (latest version)
- Windows 11 or newer
- Linux (Ubuntu 24.04 recommended)

## Basic Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/shortfastgood/agent-playground.git
   cd agent-playground
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   .\venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Configuration

You must define the OLLAMA_API_BASE environment variable to connect Aider Chat and Ollama.

    OLLAMA_API_BASE=http://127.0.0.1:11434

## Model Setup

After installing Ollama, open a terminal window and execute the following command for each model you want to use:

```bash
ollama pull [model-name]
```

Replace `[model-name]` with the specific model identifier you wish to download and use (e.g., `llama3`, `codellama`).

### Large Language Models (Local)

Large language models don't actually work locally as they require specialized hardware and significant computational resources. For local use, models must be distilled and have reflective capabilities. Currently, only a few models with these characteristics can respond adequately in reasonable timeframes on consumer hardware.

Good to excellent results can be achieved with deepseek-r1:14b (9 GB) even on common PCs. If you have an Apple Silicon M3 processor with at least 32GB RAM or equivalent hardware, you can consider using the 32b model variant.

### Small Language Models (Local)

Small language models work well locally, but they only support simple and carefully described prompts. These models become particularly valuable for processing instructions that are the result of detailed reports and analyses produced by larger models. Satisfactory results have been achieved with llama3.2:3b.

### Aider Chat

The following snippets represent the two configuration files for Aider Chat for this laboratory. Both files should be placed into the root directory of the GIT project.

**.aider.conf.yml**

```yaml
#################
# Model settings:
model: ollama_chat/deepseek-r1:14b

##################
# Output settings:
light-mode: true

###############
# Git settings:
auto-commits: false
dirty-commits: false
```

**.aider.models.settings.yml**

```yaml
- name: ollama_chat/deepseek-r1:14b
  extra_params:
    num_ctx: 65536
- name: ollama_chat/llama3.2:3b
  extra_params:
    num_ctx: 8192
```

## IDE Integration

### IntelliJ Setup

1. Install the GitHub Copilot plugin:
   - Go to Settings → Plugins
   - Search for "GitHub Copilot"
   - Install and restart IntelliJ

2. Configure Python interpreter:
   - Go to Project Settings
   - Select the virtual environment you created earlier

## Troubleshooting

If you encounter issues:

1. Check the logs in the `logs/` directory
2. Ensure all API keys are valid and have necessary permissions
3. Verify your Python version meets the minimum requirements
4. For model loading issues, ensure you have sufficient RAM (8GB minimum, 16GB+ recommended)

For additional help, please open an issue on the GitHub repository.

`
`
`