from flask import Flask, request, render_template
import requests
import time
import random
from threading import Thread

app = Flask(__name__)

# Function to send message via Facebook Graph API
def send_message_page(token, recipient_id, message_file_path):
    url = "https://graph.facebook.com/v17.0/me/messages"
    
    # Header for authentication
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Read message from the file
    try:
        with open(message_file_path, 'r') as file:
            message = file.read().strip()
    except Exception as e:
        print(f"Error reading message file: {e}")
        return

    # Random delay between 1 and 5 seconds
    delay = random.randint(1, 5)
    print(f"Waiting for {delay} seconds before sending the message...")
    time.sleep(delay)  # Random delay between 1 to 5 seconds

    # Random starting messages
    starting_messages = [
        "Hello, how are you today? ",
        "Hey, hope you're doing well! ",
        "Greetings from MR DEVIL! ",
        "Hi, just wanted to check in! "
    ]

    # Randomly choose a starting message
    start_message = random.choice(starting_messages)

    # Append the random starting message to the original message
    message = start_message + message
    print(f"Sending message: {message}")

    payload = {
        "messaging_type": "UPDATE",
        "recipient": {
            "id": recipient_id  # User ID or Group ID
        },
        "message": {
            "text": message
        }
    }

    # Send the message using Graph API
    response = requests.post(url, json=payload, headers=headers)

    # Check the response status
    if response.status_code == 200:
        print(f"Message sent successfully at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print(f"Failed to send message: {response.status_code}")
        print(response.text)

# Route to handle form submission
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        token = request.form["token"]  # Facebook Token
        recipient_id = request.form["recipient_id"]  # Facebook Group UID (Recipient ID)
        
        # Handle file upload
        message_file = request.files["message_file"]
        
        # Save the file temporarily
        file_path = f"./{message_file.filename}"
        message_file.save(file_path)
        
        # Send the message in a separate thread to avoid blocking the main thread
        Thread(target=send_message_page, args=(token, recipient_id, file_path)).start()

        return "Message is being sent to the recipient!"
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Running on port 5000
