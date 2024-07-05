import logging

from flask import Flask, render_template, request, jsonify
from datetime import datetime


logger = logging.getLogger(__name__)


app = Flask(__name__)


# Store the chat history for this session
messages = []


@app.route('/')
def index():
    logger.debug(f'Messages: {messages}')
    return render_template('chat.html', messages=messages)


@app.route('/send', methods=['POST'])
def send_message():
    user_message = request.form['message']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Format the time

    # Add user message to chat history
    messages.append({'sender': 'user', 'message': user_message, 'timestamp': timestamp})
    logging.info(f'User said: {user_message}')

    # Placeholder for AI's response logic
    ai_response = "This is where the AI's response would go."

    # Add AI response to chat history
    messages.append({'sender': 'ai', 'message': ai_response, 'timestamp': timestamp})

    return jsonify(messages)  # Return the updated chat history for the UI


if __name__ == '__main__':
    app.run(debug=True)
