import ollama

response = ollama.chat(model='llama3.1', messages=[
    {'role': 'user', 'content': 'Hello!'},
])

print(response['message']['content'])