# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands
- Run agent: `python agents/research/agent01.py --prompt <prompt_file_path>`
- Install dependencies: `pip install -r requirements.txt`
- Environment variables: Set `OLLAMA_API_BASE` for Ollama API or `GITHUB_TOKEN` for Azure

## Code Style
- Python: Follow PEP 8 guidelines with 4-space indentation
- Imports: Group standard library, third-party, and local imports
- Error handling: Use specific exceptions with clear error messages
- Documentation: Use docstrings for functions/classes (Google style)
- Configuration: Use JSON for config files with clear key naming
- Typing: Document parameter and return types in docstrings
- Naming: snake_case for functions/variables, CamelCase for classes
- File structure: Keep modules focused on single responsibility
- Error output: Print descriptive errors with context information