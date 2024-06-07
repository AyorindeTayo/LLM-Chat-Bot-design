import openai

# Set up your OpenAI API key
openai.api_key = ''

# Initialize conversation memory
conversation_history = []

def add_to_conversation_history(user_input, model_response):
    conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "assistant", "content": model_response})

def generate_response_with_memory(user_input):
    # Add the user input to the conversation history
    conversation_history.append({"role": "user", "content": user_input})
    
    # Generate response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history
    )
    
    # Get the model's response
    model_response = response['choices'][0]['message']['content']
    
    # Add the model's response to the conversation history
    conversation_history.append({"role": "assistant", "content": model_response})
    
    return model_response

def generate_joke_response(user_input):
    # Few-shot examples for generating jokes
    few_shot_prompt = [
        {"role": "system", "content": "You are an assistant who responds with humor and always includes a joke in your response."},
        {"role": "user", "content": "Tell me something interesting."}
      
    ]
    
    # Add the user input as the latest message
    few_shot_prompt.append({"role": "user", "content": user_input})
    
    # Generate response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=few_shot_prompt
    )
    
    # Get the model's response
    model_response = response['choices'][0]['message']['content']
    
    return model_response

# Function calls
def respond_with_memory(user_input):
    response = generate_response_with_memory(user_input)
    print("Assistant:", response)

def respond_with_joke(user_input):
    response = generate_joke_response(user_input)
    print("Assistant:", response)

# Command line interaction
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response_type = input("Do you want a response with memory or a joke? (memory/joke): ").strip().lower()
        if response_type == "memory":
            respond_with_memory(user_input)
        elif response_type == "joke":
            respond_with_joke(user_input)
        else:
            print("Invalid response type. Please type 'memory' or 'joke'.")
