from flask import Flask, request, jsonify
import time

# Flask app setup
app = Flask(__name__)

# Token and other configurations
PASSCODE = "MR_DEVIL123"
TARGET_NAME = "User_Name"  # Replace with actual name of the target
TARGET_USER = "User_Target_ID"  # Replace with actual target user ID
MESSAGE = "Hello, this is an automated message!"  # Message to send
MESSAGE_INTERVAL = 30  # Time interval between each message in seconds

# Function to send message (simplified example)
def send_message(token, user, message):
    print(f"Sending message to {user}: {message} using token {token}")
    # Implement message sending logic here (e.g., using an API)

# Route to handle sending messages
@app.route('/send_message', methods=['POST'])
def send_message_route():
    data = request.get_json()
    
    # Validate passcode
    passcode = data.get('passcode')
    if passcode != PASSCODE:
        return jsonify({"error": "Invalid passcode"}), 403
    
    # Get token from data
    token = data.get('token')
    if not token:
        return jsonify({"error": "Token is missing"}), 400

    # Send the message
    send_message(token, TARGET_NAME, MESSAGE)
    
    return jsonify({"message": "Message sent successfully!"}), 200

# Health check route for Render
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(debug=True)
