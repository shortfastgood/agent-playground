import argparse
import json


def load_configuration(config_path):
    """
    Load configuration from a JSON file.

    Args:
        config_path: Path to the configuration file

    Returns:
        The parsed configuration object
    """
    try:
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Configuration file not found: {config_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error parsing configuration file: {config_path}")
        return {}


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Natural Language Query Tool')
    parser.add_argument('--config', default='config.json',
                        help='Path to the configuration file (default: config.json)')
    args = parser.parse_args()
    
    # Set the configuration path
    config_path = args.config
    
    # Load configuration
    config = load_configuration(config_path)
    
    nlprompt = ""
    nlcommand = ""
    
    while True:
        # Display the prompt and get user input
        user_input = input("nlquery> ")
        
        # Check if input is a command (starts with '/')
        if user_input.startswith('/'):
            nlcommand = user_input[1:]  # Store the command without the '/' prefix
            nlprompt = ""  # Clear nlprompt as input is a command
            
            # Check if the command is 'exit' (case-insensitive)
            if nlcommand.lower() == 'exit':
                break  # Exit the program
        else:
            # Input is not a command, store it in nlprompt
            nlprompt = user_input
            nlcommand = ""  # Clear nlcommand as input is not a command

if __name__ == "__main__":
    main()
