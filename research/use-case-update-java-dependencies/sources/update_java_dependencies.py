#!/usr/bin/env python3
import argparse
import json
import logging
import os
import re
import sys
import xml.etree.ElementTree as ET
from typing import List, Optional

import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define dependency structure
class Dependency:
    def __init__(self, group_id: str, artifact_id: str, version: Optional[str] = None):
        self.group_id = group_id
        self.artifact_id = artifact_id
        self.version = version
    
    def __str__(self):
        if self.version:
            return f"{self.group_id}:{self.artifact_id}:{self.version}"
        else:
            return f"{self.group_id}:{self.artifact_id} (no version)"
    
    @property
    def has_version(self) -> bool:
        """Check if the dependency has version information"""
        return self.version is not None and self.version.strip() != ""

class DependencyUpdater:
    def __init__(self, config_path: str = "config.json", provider: str = None):
        self.provider = provider
        self.load_config(config_path)
        self.setup_ai_client()
    
    def load_config(self, config_path: str) -> None:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                self.config = json.load(f)
            logger.info(f"Configuration loaded from {config_path}")
        except Exception as e:
            logger.error(f"Failed to load configuration: {str(e)}")
            sys.exit(1)
    
    def setup_ai_client(self) -> None:
        """Set up AI client based on configuration and environment variables"""
        # Get AI configuration section
        ai_config = self.config.get("ai", {})
        
        # Use provider from command line if specified, otherwise use from config
        provider = self.provider if self.provider else ai_config.get("provider")
        
        if not provider:
            logger.error("No AI provider defined. Specify with --provider or in config file under ai.provider")
            sys.exit(1)
        
        # Convert provider names if needed (e.g., azure_openai → azure)
        if provider == "azure_openai":
            provider = "azure"
        
        if provider == "azure":
            try:
                from openai import AzureOpenAI
                api_key = os.environ.get("AZURE_API_KEY")
                if not api_key:
                    raise ValueError("AZURE_API_KEY environment variable not set")
                
                # Get Azure-specific configuration
                azure_config = ai_config.get("azure_openai", {})
                
                self.client = AzureOpenAI(
                    api_key=api_key,
                    api_version=azure_config.get("api_version", "2023-05-15"),
                    azure_endpoint=azure_config.get("endpoint")
                )
                self.ai_model = azure_config.get("model", "gpt-4o")
                logger.info("Azure OpenAI client configured")
            except Exception as e:
                logger.error(f"Failed to set up Azure OpenAI client: {str(e)}")
                sys.exit(1)
                
        elif provider == "anthropic":
            try:
                from anthropic import Anthropic
                api_key = os.environ.get("ANTHROPIC_API_KEY")
                if not api_key:
                    raise ValueError("ANTHROPIC_API_KEY environment variable not set")
                
                # Get Anthropic-specific configuration
                anthropic_config = ai_config.get("anthropic", {})
                
                self.client = Anthropic(api_key=api_key)
                self.ai_model = anthropic_config.get("model", "claude-3-sonnet-20240229")
                logger.info("Anthropic client configured")
            except Exception as e:
                logger.error(f"Failed to set up Anthropic client: {str(e)}")
                sys.exit(1)
        
        elif provider == "ollama":
            try:
                import ollama
                # Get Ollama-specific configuration
                ollama_config = ai_config.get("ollama", {})
                
                # Configure Ollama with URL from config
                ollama_url = ollama_config.get("url", "http://localhost:11434")
                
                # Create client instance with the host URL parameter
                self.client = ollama.Client(host=ollama_url)
                self.ai_model = ollama_config.get("model", "llama3.2:3b")
                logger.info(f"Ollama client configured with URL {ollama_url} and model {self.ai_model}")
            except Exception as e:
                logger.error(f"Failed to set up Ollama client: {str(e)}")
                sys.exit(1)
        else:
            logger.error(f"Unsupported AI provider: {provider}")
            sys.exit(1)
    
    def determine_file_type(self, file_path: str) -> str:
        """Determine if the file is a Gradle or Maven file"""
        if file_path.endswith("build.gradle"):
            return "gradle"
        elif file_path.endswith("pom.xml"):
            return "maven"
        else:
            logger.error(f"File {file_path} is not a recognized Gradle or Maven file")
            sys.exit(1)
    
    def read_file(self, file_path: str) -> str:
        """Read the content of a file"""
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read file {file_path}: {str(e)}")
            sys.exit(1)
    
    def parse_dependencies_with_ai(self, file_content: str, file_type: str) -> List[Dependency]:
        """Parse dependencies using AI"""
        logger.info(f"Parsing {file_type} dependencies with AI")
        
        prompt = f"""
        Parse the following {file_type} file and extract ALL dependency declarations.
        
        For Gradle files, include dependencies with any configuration (implementation, api, compileOnly, runtimeOnly, testImplementation, etc.).
        For Maven files, extract all dependencies from the dependencies section.
        
        For each dependency, identify the groupId, artifactId, and version.
        For dependencies without explicit version information, set version to null or omit the version field.
        Return the dependencies as a JSON list of objects with properties "group_id", "artifact_id", and "version" (if present).
        
        {file_content}
        """
        
        try:
            # Check provider type and use appropriate client
            if self.provider == "ollama" or (not self.provider and self.config.get("ai_provider") == "ollama"):
                response = self.client.chat(
                    model=self.ai_model,
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response['message']['content']
                
            elif self.provider == "anthropic" or (not self.provider and self.config.get("ai_provider") == "anthropic"):
                response = self.client.messages.create(
                    model=self.ai_model,
                    max_tokens=4000,
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.content[0].text
            else:  # Azure OpenAI
                response = self.client.chat.completions.create(
                    model=self.ai_model,
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content
                
            # Extract JSON from response with enhanced pattern recognition
            try:
                # Try to find JSON with standard regex (non-greedy)
                json_match = re.search(r'\[.*?\]', result, re.DOTALL)
                if json_match:
                    dependencies_json = json.loads(json_match.group(0))
                else:
                    # If no match, try to clean the entire response
                    clean_result = re.sub(r'```(?:json)?(.*?)```', r'\1', result, flags=re.DOTALL)
                    dependencies_json = json.loads(clean_result.strip())
                
                # Process dependencies
                dependencies = []
                for dep in dependencies_json:
                    version = dep.get("version") if "version" in dep else None
                    dependencies.append(Dependency(
                        dep["group_id"], 
                        dep["artifact_id"], 
                        version
                    ))
                return dependencies
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {str(e)}")
                logger.debug(f"AI response: {result}")
                sys.exit(1)
                
        except Exception as e:
            logger.error(f"AI parsing failed: {str(e)}")
            sys.exit(1)
    
    def is_milestone_or_rc(self, version: str) -> bool:
        """Check if a version is a milestone, release candidate, or alpha version"""
        return bool(re.search(r'M\d+$', version, re.IGNORECASE) or 
                    re.search(r'RC\d+$', version, re.IGNORECASE) or
                    re.search(r'alpha\d+$', version, re.IGNORECASE))
    
    def get_latest_version(self, dependency: Dependency) -> str:
        """Get latest version of a dependency from Maven central repository"""
        logger.info(f"Fetching latest version for {dependency}")
        
        base_url = self.config.get("maven_central_url", "https://repo1.maven.org/maven2")
        group_path = dependency.group_id.replace(".", "/")
        metadata_url = f"{base_url}/{group_path}/{dependency.artifact_id}/maven-metadata.xml"
        
        try:
            response = requests.get(metadata_url)
            response.raise_for_status()
            
            root = ET.fromstring(response.text)
            versioning = root.find("versioning")
            
            # Get all versions
            versions = []
            versions_elem = versioning.find("versions")
            if versions_elem is not None:
                versions = [v.text for v in versions_elem.findall("version")]
            
            # First check if there's a latest or release tag
            latest = versioning.find("latest")
            if latest is not None:
                latest_version = latest.text
                # If latest version is not a milestone/RC, use it
                if not self.is_milestone_or_rc(latest_version):
                    return latest_version
            
            # Check release tag
            release = versioning.find("release")
            if release is not None and not self.is_milestone_or_rc(release.text):
                return release.text
            
            # If we have versions, filter out milestone and RC versions
            if versions:
                stable_versions = [v for v in versions if not self.is_milestone_or_rc(v)]
                if stable_versions:
                    return stable_versions[-1]  # Return the latest stable version
                else:
                    logger.warning(f"No stable version found for {dependency}, keeping current version")
                    return dependency.version
            
            # If we couldn't find a suitable version, keep the current one
            logger.warning(f"Could not find version information for {dependency}, keeping current version")
            return dependency.version
            
        except Exception as e:
            logger.warning(f"Failed to get latest version for {dependency}: {str(e)}")
            return dependency.version  # Return current version if update fails
    
    def update_dependencies(self, dependencies: List[Dependency]) -> List[Dependency]:
        """Update dependencies to their latest versions"""
        updated_dependencies = []
        for dep in dependencies:
            # Skip dependencies without version information
            if not dep.has_version:
                logger.info(f"Skipping {dep.group_id}:{dep.artifact_id} - no version specified")
                updated_dependencies.append(dep)
                continue
                
            latest_version = self.get_latest_version(dep)
            if latest_version != dep.version:
                logger.info(f"Updating {dep.group_id}:{dep.artifact_id} from {dep.version} to {latest_version}")
                updated_dep = Dependency(dep.group_id, dep.artifact_id, latest_version)
                updated_dependencies.append(updated_dep)
            else:
                updated_dependencies.append(dep)
        return updated_dependencies
    
    def update_file_with_ai(self, file_content: str, file_type: str, 
                          original_deps: List[Dependency], updated_deps: List[Dependency]) -> str:
        """Update the file with new dependencies using AI"""
        logger.info(f"Updating {file_type} file with AI")
        
        # Create mapping of dependencies for easier reference
        updates = {}
        for i, dep in enumerate(original_deps):
            # Only include dependencies with versions in updates
            if dep.has_version and dep.version != updated_deps[i].version:
                updates[f"{dep.group_id}:{dep.artifact_id}"] = {
                    "from": dep.version,
                    "to": updated_deps[i].version
                }
        
        # If no updates needed, return original content
        if not updates:
            logger.info("No dependency updates needed")
            return file_content
        
        prompt = f"""
        Update the following {file_type} file by changing the dependency versions as specified:
        
        {json.dumps(updates, indent=2)}
        
        Here's the original file content:
        
        {file_content}
        
        Update all occurrences of these dependencies regardless of how they're declared (such as implementation, api, compile for Gradle, or any format in Maven).
        Return only the updated file content, with no additional explanation.
        """
        
        try:
            # Check provider type and use appropriate client
            if self.provider == "ollama" or (not self.provider and self.config.get("ai_provider") == "ollama"):
                response = self.client.chat(
                    model=self.ai_model,
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response['message']['content']
                
            elif self.provider == "anthropic" or (not self.provider and self.config.get("ai_provider") == "anthropic"):
                response = self.client.messages.create(
                    model=self.ai_model,
                    max_tokens=8000,
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.content[0].text
            else:  # Azure OpenAI
                response = self.client.chat.completions.create(
                    model=self.ai_model,
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content
            
            # Clean up response to get just the file content
            result = result.strip()
            # Remove markdown code blocks if present
            if result.startswith("```") and result.endswith("```"):
                result = "\n".join(result.split("\n")[1:-1])
            
            return result
            
        except Exception as e:
            logger.error(f"AI file update failed: {str(e)}")
            sys.exit(1)
    
    def write_file(self, file_path: str, content: str) -> None:
        """Write content to a file"""
        try:
            with open(file_path, 'w') as f:
                f.write(content)
            logger.info(f"Updated file written to {file_path}")
        except Exception as e:
            logger.error(f"Failed to write file {file_path}: {str(e)}")
            sys.exit(1)
    
    def update_dependencies_in_file(self, file_path: str) -> None:
        """Main method to update dependencies in a file"""
        logger.info(f"Updating dependencies in {file_path}")
        
        file_type = self.determine_file_type(file_path)
        file_content = self.read_file(file_path)
        dependencies = self.parse_dependencies_with_ai(file_content, file_type)
        
        logger.info(f"Found {len(dependencies)} dependencies")
        for dep in dependencies:
            logger.info(f"  {dep}")
        
        updated_dependencies = self.update_dependencies(dependencies)
        updated_content = self.update_file_with_ai(
            file_content, file_type, dependencies, updated_dependencies
        )
        
        self.write_file(file_path, updated_content)
        logger.info("Dependency update completed successfully")

def main():
    parser = argparse.ArgumentParser(description="Update Java dependencies in a Gradle or Maven project")
    parser.add_argument("file_path", help="Path to the build.gradle or pom.xml file")
    parser.add_argument("--conf", default="config.json", 
                        help="Path to configuration file (default: config.json)")
    parser.add_argument("--provider", choices=["azure", "anthropic", "ollama"], 
                        help="AI provider to use (overrides configuration file)")
    
    args = parser.parse_args()
    
    try:
        updater = DependencyUpdater(args.conf, args.provider)
        updater.update_dependencies_in_file(args.file_path)
    except Exception as e:
        logger.error(f"Dependency update failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
