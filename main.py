import requests
import json

model = "qwen2.5:1.5b"
ollama_url = "http://localhost:11434"
end_point = "/api/chat"
url = ollama_url + end_point

messages = []

print("Welcome to chatbot.\nWrite exit to end chat.\n ")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("By!")
        break

    messages.append({
        "role" : "user",
        "content" : user_input
    })

    payload = ({
        "model" : model,
        "messages" : messages,
        "stream" : True
    })
    try:
        response = requests.post(
            url,
            json=payload,
            timeout=120,
            stream=True
        )

        response.raise_for_status()

    except requests.exceptions.RequestException as error:
        print("Connection error", error)

    ai_text_response = []
    
    print("Rex: ", end="", flush=True)

    for line in response.iter_lines():
        if line:
            chunk = json.loads(line)
            delivered_text = chunk["message"]["content"]
            print(delivered_text, end="", flush=True)
            ai_text_response.append(delivered_text)

    displayable_message = "".join(ai_text_response)

    messages.append({
        "role" : "assistant",
        "content" : displayable_message
    })

    print()