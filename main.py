import logging
import json

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


logger = logging.getLogger(__name__)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    message_raw = db.Column(db.String(200), unique=False, nullable=False)
    timestamp = db.Column(db.DateTime)


def db_data_init():
    dt = db.session.get(User, 42)
    if not dt:
        new_user = User(id=42, username='Deep Thought')
        db.session.add(new_user)
        db.session.commit()

    mt = db.session.get(User, 1)
    if not mt:
        new_user2 = User(id=1, username='Mere Mortal')
        db.session.add(new_user2)
        db.session.commit()

    messages = Message.query.all()
    if not messages:
        message = Message(user_id=42, message_raw="Hello", timestamp=datetime.now())
        db.session.add(message)
        db.session.commit()


with app.app_context():
    db.create_all()  # Create the database tables if they don't exist
    db_data_init()  # Create some objects


class ChatData:
    user: str
    text: str
    time: str

    def __init__(self, message: Message):
        self.user = db.session.get(User, message.user_id).username
        self.text = message.message_raw
        self.time = message.timestamp.strftime('%Y-%m-%d %H:%M:%S')


def render_chat():
    messages = Message.query.all()
    data = [ChatData(message) for message in messages]
    return render_template('chat.html', messages=data)


@app.route('/')
def index():
    return render_chat()


@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        user_input = data.get('user_input')
        user_message = Message(user_id=1, message_raw=user_input, timestamp=datetime.now())
        db.session.add(user_message)
        db.session.commit()
    except Exception as e:
        logger.debug("Could not parse the input: %s", e)

    # TODO: render just the json
    return render_chat()


if __name__ == '__main__':
    app.run(debug=True)
