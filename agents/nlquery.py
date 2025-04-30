import argparse
import json
import logging
import psycopg2
import os
import sys
import re
from typing import Optional, Dict, Any
from tabulate import tabulate  # Add tabulate for pretty table formatting

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Global variables
tables_list = ""
current_schema = None  # Store the currently selected schema
current_query = ""     # Store the currently extracted SQL query

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


def setup_ai_client(config: Dict[str, Any], provider: str = None) -> Optional[Any]:
    """
    Set up an AI client based on the specified provider.
    
    Args:
        config: Configuration dictionary containing AI service parameters
        provider: The AI provider to use ('azure', 'anthropic', 'ollama')
                 If None, uses the provider specified in config
    
    Returns:
        An initialized AI client if successful, None otherwise
    """
    # Get AI configuration from config
    ai_config = config.get('ai', {})
    
    # If provider is not specified, get from config
    if provider is None:
        provider = ai_config.get('provider', '').lower()
    else:
        provider = provider.lower()
    
    try:
        if provider == 'azure_openai':
            try:
                from openai import AzureOpenAI
            
                azure_config = ai_config.get('azure_openai', {})
                azure_api_key = os.environ.get("AZURE_API_KEY")
                if not azure_api_key:
                    raise ValueError("AZURE_API_KEY environment variable not set")
            
                client = AzureOpenAI(
                    api_key=azure_api_key,
                    api_version=azure_config.get('api_version', '2024-12-01-preview'),
                    azure_endpoint=azure_config.get('endpoint', os.getenv('AZURE_OPENAI_ENDPOINT'))
                )
                print(f"Azure OpenAI client initialized successfully")
                return {
                    "client": client,
                    "model": azure_config.get('model', 'gpt-4o')
                }
            except Exception as e:
                logger.error(f"Failed to set up Azure OpenAI client: {str(e)}")
                sys.exit(1)
            
        elif provider == 'anthropic':
            try:
                from anthropic import Anthropic
            
                anthropic_config = ai_config.get('anthropic', {})   
                anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
                if not anthropic_api_key:
                    raise ValueError("ANTHROPIC_API_KEY environment variable not set")
                client = Anthropic(
                    api_key=anthropic_api_key
                )
                print(f"Anthropic client initialized successfully")
                return {
                    "client": client,
                    "model": anthropic_config.get('model', 'claude-3-7-sonnet-20250219')
                }
            except Exception as e:
                logger.error(f"Failed to set up Anthropic client: {str(e)}")
                sys.exit(1)
            
        elif provider == 'ollama':
            try:
                import ollama
                
                ollama_config = ai_config.get('ollama', {})
                # Configure Ollama with URL from config
                url = ollama_config.get("url", "http://localhost:11434")
                # Create client instance with the host URL parameter
                client = ollama.Client(host=url)
                model = ollama_config.get("model", "llama3.2b")
                logger.info(f"Ollama client configured with URL {url} and model {model}")
                return {
                    "client" : client,
                    "model" : model
                }
            except Exception as e:
                logger.error(f"Failed to set up Ollama client: {str(e)}")
                sys.exit(1)
            
        else:
            print(f"Unsupported AI provider: {provider}")
            return None
            
    except ImportError as e:
        print(f"Error loading required packages for {provider}: {e}")
        print(f"Try installing the required package with: pip install <package>")
        return None
    except Exception as e:
        print(f"Error initializing {provider} client: {e}")
        return None


def parse_prompt(ai_client_config: Dict[str, Any], prompt: str) -> str | None | Any:
    """
    Process a natural language prompt using the configured AI client.
    
    Args:
        ai_client_config: Dictionary containing the AI client and model information
        prompt: The natural language prompt to process
        
    Returns:
        The AI-generated response as a string
    """
    global current_schema, tables_list, current_query
    
    # Clear current_query before processing new prompt
    current_query = ""
    
    if not ai_client_config or not prompt:
        return "Error: AI client not configured or prompt is empty."
    
    client = ai_client_config.get("client")
    model = ai_client_config.get("model")
    
    try:
        # Format the system message with database context
        system_message = """You are a helpful database assistant. 
        Help the user understand and work with their PostgreSQL database. 
        When writing SQL queries, format them clearly and explain what they do.
        Always put SQL queries in code blocks using ```sql and ``` syntax.
        Be concise and accurate in your responses."""
        
        # Get schema information if current_schema is set
        schema_ddl = ""
        if current_schema:
            try:
                # Get configuration from the main function's scope
                config = load_configuration('config.json')  # Use default config path
                connection = connect_to_database(config)
                if connection:
                    get_database_tables_by_schema(connection, current_schema)
                    schema_ddl = generate_ddl(connection, current_schema)
                    connection.close()
                    
                    # Add the schema information to the system message
                    system_message += f"\n\nCurrent schema: {current_schema}\n"
                    system_message += f"Available tables: {tables_list}\n"
                    system_message += f"Schema DDL:\n{schema_ddl}"
            except Exception as e:
                logger.error(f"Error retrieving schema DDL: {str(e)}")
        
        # Process based on provider type and collect the response
        llm_response = None
        
        if isinstance(client, dict) and "provider" in client:
            provider = client["provider"]
            
            if provider == "azure_openai":
                response = client["client"].chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": prompt}
                    ]
                )
                llm_response = response.choices[0].message.content
                
            elif provider == "anthropic":
                response = client["client"].messages.create(
                    model=model,
                    system=system_message,
                    messages=[{"role": "user", "content": prompt}]
                )
                llm_response = response.content[0].text
                
            elif provider == "ollama":
                response = client["client"].generate(
                    model=model,
                    prompt=f"{system_message}\n\nUser: {prompt}\n\nAssistant:",
                    stream=False
                )
                llm_response = response.get("response", "No response generated")

        # Handle specific client types directly
        elif hasattr(client, "chat") and hasattr(client.chat, "completions"):
            # Azure OpenAI client
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ]
            )
            llm_response = response.choices[0].message.content
            
        elif hasattr(client, "messages") and hasattr(client.messages, "create"):
            # Anthropic client
            response = client.messages.create(
                model=model,
                system=system_message,
                messages=[{"role": "user", "content": prompt}]
            )
            llm_response = response.content[0].text
            
        elif hasattr(client, "generate"):
            # Ollama client
            response = client.generate(
                model=model,
                prompt=f"{system_message}\n\nUser: {prompt}\n\nAssistant:",
                stream=False
            )
            llm_response = response.get("response", "No response generated")
            
        else:
            return "Error: Unsupported AI client type."

        # logger.info(llm_response)

        # Extract SQL code blocks from the response using regex
        if llm_response:
            sql_matches = re.findall(r'```sql\n(.*?)\n```', llm_response, re.DOTALL)
            if sql_matches:
                current_query = sql_matches[0].strip()
                # logger.info(f"Extracted SQL query: {current_query}")
        
        return llm_response
            
    except Exception as e:
        logger.error(f"Error processing prompt with AI: {str(e)}")
        return f"Error processing your request: {str(e)}"


def connect_to_database(config):
    """
    Establish a connection to the PostgreSQL database using configuration parameters.
    
    Args:
        config: Configuration dictionary containing database connection parameters
        
    Returns:
        A database connection object if successful, None otherwise
    """
    try:
        # Extract database connection parameters from config
        db_config = config.get('database', {})
        
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            host=db_config.get('host', 'localhost'),
            port=db_config.get('port', 5432),
            database=db_config.get('name', ''),
            user=db_config.get('user', ''),
            password=db_config.get('password', '')
        )
        
        return connection
    
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None


def get_database_schemas(connection):
    """
    Query and retrieve a list of all schemas in the database.
    
    Args:
        connection: A PostgreSQL database connection object
        
    Returns:
        A list of schema names if successful, empty list otherwise
    """
    try:
        cursor = connection.cursor()
        
        # Query to get all schemas in the database
        cursor.execute("SELECT schema_name FROM information_schema.schemata")
        
        # Fetch all results
        schemas = [row[0] for row in cursor.fetchall()]
        
        cursor.close()
        return schemas
        
    except psycopg2.Error as e:
        print(f"Error retrieving database schemas: {e}")
        return []


def get_database_tables_by_schema(connection, schema_name):
    """
    Query and retrieve a list of all tables in a specific schema.
    
    Args:
        connection: A PostgreSQL database connection object
        schema_name: Name of the schema to query tables from
        
    Returns:
        A list of table names in the specified schema if successful, empty list otherwise
    """
    global tables_list
    
    try:
        cursor = connection.cursor()
        
        # Query to get all tables in the specified schema
        cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = %s",
            (schema_name,)
        )
        
        # Fetch all results
        tables = [row[0] for row in cursor.fetchall()]
        
        # Format table names with schema name and create comma-separated string
        formatted_tables = [f"{schema_name}.{table}" for table in tables]
        tables_list = ",".join(formatted_tables)
        
        cursor.close()
        return tables
        
    except psycopg2.Error as e:
        print(f"Error retrieving tables for schema '{schema_name}': {e}")
        return []


def get_table_structure(connection, schema_name, table_name):
    """
    Query and retrieve the structure of a specific table in a schema.
    
    Args:
        connection: A PostgreSQL database connection object
        schema_name: Name of the schema containing the table
        table_name: Name of the table to get structure for
        
    Returns:
        A list of dictionaries containing column information if successful, empty list otherwise
    """
    try:
        cursor = connection.cursor()
        
        # Query to get column information for the specified table
        query = """
            SELECT 
                column_name, 
                data_type, 
                character_maximum_length,
                is_nullable,
                column_default
            FROM 
                information_schema.columns 
            WHERE 
                table_schema = %s 
                AND table_name = %s
            ORDER BY 
                ordinal_position
        """
        
        cursor.execute(query, (schema_name, table_name))
        
        # Fetch all results and format them as dictionaries
        columns = []
        for row in cursor.fetchall():
            column_info = {
                'name': row[0],
                'data_type': row[1],
                'max_length': row[2],
                'is_nullable': row[3],
                'default_value': row[4]
            }
            columns.append(column_info)
        
        cursor.close()
        return columns
        
    except psycopg2.Error as e:
        print(f"Error retrieving structure for table '{schema_name}.{table_name}': {e}")
        return []


def generate_ddl(connection, schema_name):
    """
    Generate DDL (Data Definition Language) statements for all tables in a specific schema.
    
    Args:
        connection: A PostgreSQL database connection object
        schema_name: Name of the schema to generate DDL for
        
    Returns:
        A string containing all DDL statements for the tables in the schema
    """
    # Get all tables in the specified schema
    tables = get_database_tables_by_schema(connection, schema_name)
    
    if not tables:
        return f"No tables found in schema '{schema_name}'."
    
    # Initialize an empty list to store the DDL statements
    ddl_statements = []
    
    # Process each table
    for table_name in tables:
        # Get the structure of the table
        columns = get_table_structure(connection, schema_name, table_name)
        
        if not columns:
            ddl_statements.append(f"-- Could not retrieve structure for '{schema_name}.{table_name}'")
            continue
        
        # Start building the CREATE TABLE statement
        ddl = f"CREATE TABLE {schema_name}.{table_name} (\n"
        
        # Add column definitions
        column_definitions = []
        for column in columns:
            # Start with column name and data type
            column_def = f"    {column['name']} {column['data_type']}"
            
            # Add character length if applicable
            if column['max_length'] is not None:
                column_def += f"({column['max_length']})"
            
            # Add NULL/NOT NULL constraint
            if column['is_nullable'] == 'NO':
                column_def += " NOT NULL"
            
            # Add default value if present
            if column['default_value'] is not None:
                column_def += f" DEFAULT {column['default_value']}"
            
            column_definitions.append(column_def)
        
        # Join column definitions with commas
        ddl += ",\n".join(column_definitions)
        
        # Close the CREATE TABLE statement
        ddl += "\n);"
        
        ddl_statements.append(ddl)
    
    # Join all DDL statements with double line breaks
    return "\n\n".join(ddl_statements)


def execute_query(sql_query, config=None):
    """
    Execute an SQL query and display the results as a formatted table.
    
    Args:
        sql_query: SQL query string to execute
        config: Configuration dictionary containing database connection parameters
               If None, uses the default config.json
    
    Returns:
        True if execution was successful, False otherwise
    """
    if not sql_query:
        print("Error: No SQL query provided.")
        return False
    
    # Load config if not provided
    if config is None:
        config = load_configuration('config.json')
    
    connection = connect_to_database(config)
    if not connection:
        print("Failed to connect to the database. Please check your configuration.")
        return False
    
    try:
        # Create cursor
        cursor = connection.cursor()
        
        # Execute query
        cursor.execute(sql_query)
        
        # Check if query returns results (SELECT, SHOW, etc.)
        if cursor.description:
            # Get column names from cursor description
            columns = [desc[0] for desc in cursor.description]
            
            # Fetch all results
            results = cursor.fetchall()
            
            # Display results as a table
            if results:
                print(f"\nQuery executed successfully. {len(results)} rows returned.\n")
                print(tabulate(results, headers=columns, tablefmt="psql"))
            else:
                print("\nQuery executed successfully. No rows returned.")
        else:
            # For non-SELECT queries (INSERT, UPDATE, DELETE, etc.)
            row_count = cursor.rowcount
            connection.commit()  # Commit changes for DML statements
            print(f"\nQuery executed successfully. {row_count} rows affected.")
        
        # Close cursor
        cursor.close()
        return True
        
    except psycopg2.Error as e:
        print(f"Error executing query: {e}")
        connection.rollback()  # Rollback any changes in case of error
        return False
    finally:
        connection.close()


def display_schemas(schemas):
    """
    Format and display database schema information.
    
    Args:
        schemas: List of schema names retrieved from the database
    """
    if not schemas:
        print("No schemas found in the database.")
        return
        
    print("\nAvailable database schemas:")
    print("=" * 30)
    
    for i, schema in enumerate(schemas, 1):
        print(f"{i}. {schema}")
    
    print("=" * 30)
    print(f"Total schemas: {len(schemas)}\n")


def display_tables(schema_name, tables):
    """
    Format and display database table information for a specific schema.
    
    Args:
        schema_name: Name of the schema containing the tables
        tables: List of table names retrieved from the database
    """
    if not tables:
        print(f"No tables found in the schema '{schema_name}'.")
        return
        
    print(f"\nTables in schema '{schema_name}':")
    print("=" * 40)
    
    for i, table in enumerate(tables, 1):
        print(f"{i}. {table}")
    
    print("=" * 40)
    print(f"Total tables: {len(tables)}\n")


def display_table_structure(schema_name, table_name, columns):
    """
    Format and display the structure of a database table.
    
    Args:
        schema_name: Name of the schema containing the table
        table_name: Name of the table
        columns: List of dictionaries containing column information
    """
    if not columns:
        print(f"No column information found for table '{schema_name}.{table_name}'.")
        return
        
    print(f"\nStructure of table '{schema_name}.{table_name}':")
    print("=" * 160)
    
    # Print header
    print(f"{'Column Name':<25} {'Data Type':<30} {'Max Length':<10} {'Nullable':<10} {'Default':<30}")
    print("-" * 160)
    
    # Print each column's details
    for column in columns:
        name = column['name']
        data_type = column['data_type']
        max_length = str(column['max_length']) if column['max_length'] is not None else 'N/A'
        is_nullable = 'YES' if column['is_nullable'] == 'YES' else 'NO'
        default_value = str(column['default_value']) if column['default_value'] is not None else 'NULL'
        
        print(f"{name:<25} {data_type:<30} {max_length:<10} {is_nullable:<10} {default_value:<30}")
    
    print("=" * 160)
    print(f"Total columns: {len(columns)}\n")


def display_help():
    """
    Display a list of all available commands with short descriptions.
    """
    print("\nAvailable Commands:")
    print("=" * 80)
    print("/help                            - Display this help message")
    print("/exit                            - Exit the program")
    print("/clear                           - Reset all global variables")
    print("/schema <schema_name>            - Set the current working schema")
    print("/schemas                         - List all available database schemas")
    print("/tables <schema_name>            - List all tables in a specific schema")
    print("/table <schema_name> <table_name> - Show structure of a specific table")
    print("/ddl <schema_name>               - Generate DDL statements for all tables in a schema")
    print("/exec                            - Execute the last extracted SQL query (shorthand)")
    print("/execute                         - Execute the last extracted SQL query")
    print("/execute <custom_sql>            - Execute a custom SQL query")
    print("=" * 80)
    print("For any other input, the system will process it as a natural language query")
    print("to the AI assistant about the database.\n")


def main():
    # Declare global variables at the beginning of the function
    global tables_list, current_schema, current_query
    
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
            
            # Handle the 'help' command to display available commands
            elif nlcommand.lower() == 'help':
                display_help()
            
            # Handle the 'clear' command to reset all global variables
            elif nlcommand.lower() == 'clear':
                tables_list = ""
                current_schema = None
                print("All global variables have been reset.")
            
            # Handle the 'schema <schema_name>' command to set the current schema
            elif nlcommand.lower().startswith('schema '):
                # Extract schema name from the command
                current_schema = nlcommand[7:].strip()
                
                if not current_schema:
                    print("Error: Schema name is required. Usage: /schema <schema_name>")
                else:
                    print(f"Current schema set to '{current_schema}'")
                    
                    # Verify the schema exists
                    connection = connect_to_database(config)
                    if connection:
                        try:
                            schemas = get_database_schemas(connection)
                            if current_schema in schemas:
                                print(f"Schema '{current_schema}' found in the database.")
                            else:
                                print(f"Warning: Schema '{current_schema}' not found in the database.")
                        finally:
                            connection.close()
                    else:
                        print("Failed to connect to the database. Please check your configuration.")
            
            # Handle the 'schemas' command to retrieve database schemas
            elif nlcommand.lower() == 'schemas':
                print("Retrieving database schemas...")
                connection = connect_to_database(config)
                
                if connection:
                    try:
                        schemas = get_database_schemas(connection)
                        display_schemas(schemas)
                    finally:
                        connection.close()
                else:
                    print("Failed to connect to the database. Please check your configuration.")
                    
            # Handle the 'tables <schema_name>' command to retrieve tables from a specific schema
            elif nlcommand.lower().startswith('tables '):
                # Extract schema name from the command
                schema_name = nlcommand[7:].strip()
                
                if not schema_name:
                    print("Error: Schema name is required. Usage: /tables <schema_name>")
                else:
                    print(f"Retrieving tables for schema '{schema_name}'...")
                    connection = connect_to_database(config)
                    
                    if connection:
                        try:
                            tables = get_database_tables_by_schema(connection, schema_name)
                            display_tables(schema_name, tables)
                        finally:
                            connection.close()
                    else:
                        print("Failed to connect to the database. Please check your configuration.")
            
            # Handle the 'table <schema_name> <table_name>' command to retrieve table structure
            elif nlcommand.lower().startswith('table '):
                # Split the command into parts to extract schema and table names
                parts = nlcommand.split()
                
                if len(parts) < 3:
                    print("Error: Schema name and table name are required. Usage: /table <schema_name> <table_name>")
                else:
                    schema_name = parts[1]
                    table_name = parts[2]
                    
                    print(f"Retrieving structure for table '{schema_name}.{table_name}'...")
                    connection = connect_to_database(config)
                    
                    if connection:
                        try:
                            columns = get_table_structure(connection, schema_name, table_name)
                            display_table_structure(schema_name, table_name, columns)
                        finally:
                            connection.close()
                    else:
                        print("Failed to connect to the database. Please check your configuration.")
            
            # Handle the 'ddl <schema_name>' command to generate DDL statements for a schema
            elif nlcommand.lower().startswith('ddl '):
                # Extract schema name from the command
                schema_name = nlcommand[4:].strip()
                
                if not schema_name:
                    print("Error: Schema name is required. Usage: /ddl <schema_name>")
                else:
                    print(f"Generating DDL for schema '{schema_name}'...")
                    connection = connect_to_database(config)
                    
                    if connection:
                        try:
                            ddl_statements = generate_ddl(connection, schema_name)
                            print(ddl_statements)
                        finally:
                            connection.close()
                    else:
                        print("Failed to connect to the database. Please check your configuration.")
                
            # Handle the 'exec' command to execute the current SQL query
            elif nlcommand.lower() == 'exec':
                if not current_query:
                    print("Error: No SQL query to execute. First generate a query using natural language.")
                else:
                    print(f"Executing SQL query:\n{current_query}\n")
                    execute_query(current_query, config)
                
            # Handle the 'execute' command to execute SQL queries
            elif nlcommand.lower().startswith('execute'):
                # Check if a custom query is provided after 'execute'
                custom_query = nlcommand[8:].strip() if len(nlcommand) > 8 else None
                
                # If custom query is provided, use it; otherwise use the last extracted query
                query_to_execute = custom_query if custom_query else current_query
                
                if not query_to_execute:
                    print("Error: No SQL query to execute. Use '/execute <sql_query>' or first generate a query.")
                else:
                    print(f"Executing SQL query:\n{query_to_execute}\n")
                    execute_query(query_to_execute, config)
            else:
                print(f"Unknown command: {nlcommand}")
        else:
            # Input is not a command, store it in nlprompt
            nlprompt = user_input
            nlcommand = ""  # Clear nlcommand as input is not a command
            # Process the natural language prompt using the AI client
            response = parse_prompt(setup_ai_client(config), nlprompt)
            if response:
                print(f"AI Response: {response}")
            else:
                print("Error processing the prompt. Please check your input or configuration.")

if __name__ == "__main__":
    main()
