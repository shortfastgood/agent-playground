# Models Research

This document explores various language models that can be used within the agent playground for software development assistance.

The additional tools and models used in this section are listed in [tools/installation.md](tools/installation.md).

## Large Language Models (LLM)

Large Language Models are powerful AI systems trained on vast amounts of data, capable of understanding context and generating human-like text. In our agent-playground project, these models serve as the reflective layer for code analysis and understanding.

### Key LLMs for Consideration

The target of the project is to run the models locally, but at the moment, only a few models can be run locally on consumer hardware. 
Due to the long response times of the  current local installation the development of the agent would take too long, 
so we are using the models available on the cloud. The two model chosen are:

1. **GPT-4** and variants
   - Capabilities: Strong code understanding, can analyze complex codebases, generate fixes
   - Integration: Available via OpenAI API, GitHub Copilot
   - Limitations: Latency, token limits
   - Advantages: unlimited use with GitHub Copilot

2. **Claude 3.7 Sonnet**
   - Capabilities: Advanced reasoning, longer context windows, strong code analysis
   - Integration: Anthropic API, available via GitHub Copilot
   - Advantages: Better at following complex instructions, high accuracy on code tasks
   - Limitations: 240 free requests per month, then 0.04 USD per request on GitHub Copilot

## LLMs for Local Usage

1. **Deepseek-R1**
   - Capabilities: Open-source model with strong performance
   - Integration: Can be run locally on consumer hardware
   - Use case: Code analysis, generation, and debugging
   - Limitations: May require significant resources for larger models
   - Advantages: No API costs, full control over the model
   - Disadvantages: Requires setup and maintenance, may not match cloud models in performance

## Small Language Models (SLM)

Small Language Models are more efficient, focused models that can run with fewer resources. 
In our architecture, these can handle specific, well-defined tasks in parallel.

### Key SLMs for Consideration

1. **Llama3.2**
   - Capabilities: Efficient model with strong performance/size ratio
   - Integration: Can run on edge devices or with minimal cloud resources
   - Use case: Quick code reviews, linting, simple pattern detection
   - Limitations: May not handle complex codebases as well as larger models
   - Advantages: Lower operational costs, faster response times

## Model Selection Criteria for PR Review

For our Digital Banking PR review use case, the following criteria guide model selection:

1. **Accuracy**: How well the model understands code semantics, not just syntax
2. **Speed**: Response time for analyzing PRs of typical size
3. **Cost**: Operational expenses for model inference
4. **Integration**: Ease of connecting to GitHub workflows
5. **Explainability**: Ability to justify and explain recommendations

## Implementation Strategy

Our implementation will likely use a hybrid approach:

1. Use SLMs for initial screening, linting, and pattern detection
2. Escalate complex analysis to LLMs when necessary
3. Maintain a knowledge base of common issues and solutions to optimize responses

This tiered approach should balance cost, performance, and accuracy while meeting the project's goal of reducing senior developer time spent on routine PR reviews.
