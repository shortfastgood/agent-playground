# Installation Guide

This document outlines the steps to set up your development environment for the Agent Playground project.

## Prerequisites

Ensure you have the following installed on your system:

- Python 3.12+
- Git
- A text editor or IDE (Intellij Ultimate recommended, as used in the project)
- GitHub account with GitHub Copilot subscription (for AI-assisted development)
- [Ollama](https://ollama.com) LLM runner (for local model inference)

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

1. Create a `.env` file in the project root with the following settings:
   ```
   # API Keys (if applicable)
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   
   # Configuration
   MODEL_PROVIDER=openai  # or anthropic, local, etc.
   LOG_LEVEL=info
   ```

2. Configure GitHub integration:
   - Generate a Personal Access Token with `repo` scope
   - Add to your `.env` file:
   ```
   GITHUB_TOKEN=your_github_token
   ```

## Model Setup

### Large Language Models (Cloud-based)

For cloud-based LLMs, ensure you have:
- Valid API keys added to your `.env` file
- Sufficient API quota/credits for your usage

### Small Language Models (Local)

For local inference:
1. Install additional dependencies:
   ```bash
   pip install -r requirements-local.txt
   ```

2. Download model weights:
   ```bash
   python tools/download_models.py --model codellama-7b
   ```

## Verification

Verify your installation is working:
```bash
python -m agent_playground.verify_setup
```

This should output a confirmation that all components are correctly installed and configured.

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
