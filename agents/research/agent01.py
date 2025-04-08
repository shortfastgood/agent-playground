import json
import requests
import os
import argparse
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

class Agent:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Load options instead of temperature, default to empty object if not defined
        self.options = self.config.get("modelOptions", {})
        
        self.model = self.config.get("model", "")

    def query_ollama(self, prompt, options=None):
        """
        Query the Ollama model with the given prompt and options
        """
        if options is None:
            options = self.options
            
        payload = {
            "model": self.model,
            "prompt": prompt,
            "options": options,
            "format": "json",
            "stream": False
        }
        
        # Use OLLAMA_API_BASE environment variable with fallback to 127.0.0.1
        base_url = os.environ.get("OLLAMA_API_BASE", "http://127.0.0.1:11434")
        api_endpoint = f"{base_url}/api/generate"
        
        response = requests.post(api_endpoint, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

    def query_azure(self, prompt, options=None):
        """
        Query the Azure OpenAI service with the given prompt and options
        """
        if options is None:
            options = self.options
        
        # Extract necessary configuration for Azure
        azure_endpoint = self.config.get("azure_endpoint", "")
        azure_api_key = os.environ.get("GITHUB_TOKEN", "")
        
        if not azure_endpoint or not azure_api_key:
            print("Error: Azure OpenAI endpoint or GitHub token not set in config or environment variables.")
            return None
        
        try:
            # Create a client for the Azure OpenAI service
            client = ChatCompletionsClient(
                endpoint=azure_endpoint, 
                credential=AzureKeyCredential(azure_api_key)
            )
            
            # Create the messages for the chat completion
            messages = [{"role": "user", "content": prompt}]
            
            # Extract deployment name from azure_model or fallback to model or default
            deployment_name = self.config.get("azure_model") or self.model or "gpt-4"
            
            # Extract parameters from options if they exist
            temperature = options.get("temperature")
            top_p = options.get("top_p")
            max_tokens = options.get("max_tokens")
            
            # Call the Azure OpenAI service with parameters directly
            response = client.complete(
                deployment_name=deployment_name,
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens
            )
            
            # Format the response similar to the Ollama response
            formatted_response = {
                "model": self.model,
                "created_at": str(response.created_at),
                "response": response.choices[0].message.content,
                "done": True
            }
            
            return formatted_response
        
        except Exception as e:
            print(f"Error querying Azure OpenAI: {str(e)}")
            return None

def collect_java_files(scan_directory):
    """
    Recursively collect all Java files (.java) in the given directory.
    
    Args:
        scan_directory (str): Directory path to scan for Java files
    
    Returns:
        list: List of paths to Java files found
    """
    java_files = []
    
    # Check if the directory exists
    if not os.path.isdir(scan_directory):
        print(f"Error: Directory {scan_directory} does not exist.")
        return java_files
    
    # Walk through directory structure recursively
    for root, _, files in os.walk(scan_directory):
        for file in files:
            if file.endswith(".java"):
                java_files.append(os.path.join(root, file))
    
    return java_files

def validate_prompt_file(file_path):
    """
    Validate that the prompt file exists and is readable, then return its contents.
    
    Args:
        file_path (str): Path to the prompt file
    
    Returns:
        str: Content of the prompt file if valid, None otherwise
    """
    if not os.path.exists(file_path):
        print(f"Error: Prompt file {file_path} does not exist.")
        return None
    
    if not os.path.isfile(file_path):
        print(f"Error: {file_path} is not a file.")
        return None
    
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except IOError:
        print(f"Error: Could not read prompt file {file_path}.")
        return None

def main():
    """Main function for agent01."""
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Process Java files with Ollama")
    parser.add_argument("--prompt", required=True, help="Path to the prompt file")
    args = parser.parse_args()
    
    # Validate the prompt file
    prompt_content = validate_prompt_file(args.prompt)
    if prompt_content is None:
        return
    
    print(f"Prompt file loaded: {args.prompt}")
    
    config_path = "./agents/research/config.json"
    if not os.path.exists(config_path):
        print("Error: config.json not found in the working directory.")
        return
    
    agent = Agent(config_path)
    
    scandir = agent.config.get("scandir")
    report = agent.config.get("report")
    
    print(f"Configuration loaded successfully:")
    print(f"- Scan directory: {scandir}")
    print(f"- Report file: {report}")
    print(f"- Model: {agent.model}")

    # Collect Java files
    print(f"Scanning for Java files in {scandir}...")
    java_files = collect_java_files(scandir)
    print(f"Found {len(java_files)} Java files.")
    
    # Print the first few files as a sample
    if java_files:
        print("Sample of found Java files:")
        for file in java_files[:5]:  # Show up to 5 files
            print(f"  - {file}")
        if len(java_files) > 5:
            print(f"  ... and {len(java_files) - 5} more.")
        
        # Process Java files with Ollama using the provided prompt
        print("Processing Java files with Ollama...")
        for file_path in java_files:
            try:
                with open(file_path, 'r') as file:
                    java_content = file.read()
                    
                    # Combine prompt with Java content
                    combined_prompt = f"{prompt_content}\n\nJava code:\n```java\n{java_content}\n```"
                    
                    response = agent.query_ollama(combined_prompt)

                    if response is None:
                        print(f"Error: No response from Ollama for {file_path}")
                        continue
                    elif not response["done"]:
                        print(f"Warning: Response not complete for {file_path}")
                        continue
                    
                    # Here you could save or process the response
                    # This is a placeholder for actual response handling
                    print(f"Processed {file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")

if __name__ == "__main__":
    main()
