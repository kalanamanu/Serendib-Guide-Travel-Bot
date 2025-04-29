from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

RASA_URL = 'http://localhost:5005/webhooks/rest/webhook'  # Rasa URL

@app.route('/')
def home():
    return render_template('index.html')  # You'll create this later

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'response': "No message received."}), 400

    try:
        response = requests.post(RASA_URL, json={"sender": "user", "message": user_message})
        messages = response.json()
        if messages:
            bot_reply = " ".join([msg.get("text", "") for msg in messages])
        else:
            bot_reply = "Sorry, I didn't understand that."

        return jsonify({'response': bot_reply})

    except Exception as e:
        return jsonify({'response': f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
