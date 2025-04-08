# Prompts to generate the agent01

1. into the subfolder agents/research I need a new python program called agent01 and a configration file called config.json. The configuration file should have two properties "scandir": "../ifps" and "report": "./research/report01.txt. The program should read the configuration from the working directory.
2. I wish a new function to connect to ollama using the environment variable OLLAMA_API_BASE. The function should accept the content of a single java file as first argument, a prompt as second argument, the model as third parameter and the temperature to use as fourth argument. The function should pass the inforamtion to ollama and wait for the answer, then give the result back to the caller. Update requirements.txt if necessary
3. Add to agent01 the parameter --prompt that should point to the path to a prompt file. Agent01 should check the path to be sure the file exists and is readable. Update requirements.txt if necessary.
4. 'Error connecting to Ollama API: Extra data: line 2 column 1 (char 98)'
5. I wish to improve the numer of token handled by ollama. Add the property 'maxTokens': '65536' to the configuration. Pass the new property to query_ollama and forward it to the ollama runner
6. In the configuration add a new object "modelOptions". Move temperature inside modelOptions. Add "num_ctx": "8192", "top_k": "40", "top_p": "0.9" and "min_p": "0.0" to modelOptions
7. The agent01 should load options instead of temperature, if options isn't defined replace it with an empy object. The printout of the temperature should be removed. query_ollama should accept options instead of temperature. The payload should be modified to send the entire options object instead of temperature. Add to "fomat": "json" to the payload
8. The prompt passed to the new ollama agent is build using the prompt_content and the java content. The java_content is passed explicitely as java snippet.
9. To connect to ollama agent01 must use environment variable OLLAMA_API_BASE. Use always 127.0.0.1 instead of localhost.
10. Agent01: add to the agent class the function query_azure with the same arguments of query ollama. The implementation, instead should use the ChatCompletitionsClient of the package azure-ai-inference. Update requirements.txt if necessary
11. Agent01: replace AZURE_OPENAI_API_KEY with GITHUB_TOKEN, add "azure_endpoint":"https://models.inference.ai.azure.com" to config.json and use this property instead of the environment variable in query_azure
12. Add "azure_model": "DeepSeek-R1" to config.json and use the property instead of model in query_azure
13. Agent01, query_azure there is no azure_options, temperature, top_p and max_tokens are arguments of client.complete