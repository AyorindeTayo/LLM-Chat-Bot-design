from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

# Set up your OpenAI API key
openai.api_key = ''

# Initialize conversation memory for each user
user_conversations = {}

def generate_response_with_memory(username, user_input):
    # Initialize user conversation if not already done
    if username not in user_conversations:
        user_conversations[username] = []

    conversation_history = user_conversations[username]

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
    
    # Update the user's conversation history
    user_conversations[username] = conversation_history
    
    return model_response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    username = data.get('username')
    question = data.get('question')
    
    if not username or not question:
        return jsonify({'error': 'Missing username or question'}), 400

    response = generate_response_with_memory(username, question)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
