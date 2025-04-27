from flask import Flask, request,redirect
import time

app = Flask(__name__)

# Function to read files and get the required configurations
def read_file(file_name):
    try:
        with open(file_name, 'r') as file:
            return file.read().strip()
    except Exception as e:
        return str(e)

# Read data from respective files
TOKEN = read_file('TOKEN.txt')  # Read token from TOKEN.txt
MESSAGE = read_file('FILE.txt')  # Read message from FILE.txt
TARGET_UID = read_file('CONVO.txt')  # Read target user ID from CONVO.txt
MESSAGE_INTERVAL = int(read_file('SPEED.txt'))  # Read speed from SPEED.txt

# Function to simulate sending a message
def send_message(token, user_id, message):
    # Simulating sending the message (you can replace it with actual API calls)
    print(f"Sending message to {user_id}: {message} using token {token}")
    # Here you would use the actual API to send a message using the token.

# Route to handle sending messages
@app.route('/send_message', methods=['POST'])
def send_message_route():
    # Request data
    data = request.get_json()
    
    # Validate passcode from the request body
    passcode = data.get('passcode')
    if passcode != "MR_DEVIL123":  # Check passcode
        return jsonify({"error": "Invalid passcode"}), 403
    
    # Sending message every MESSAGE_INTERVAL seconds
    try:
        while True:
            send_message(TOKEN, TARGET_UID, MESSAGE)  # Send message
            time.sleep(MESSAGE_INTERVAL)  # Wait for the specified interval before sending next message
    except KeyboardInterrupt:
        return jsonify({"error": "Message sending interrupted"}), 500

    return jsonify({"message": "Message sent successfully!"}), 200

# Health check route to confirm the server is working
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(debug=True)
