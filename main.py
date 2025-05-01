from flask import Flask, request
import requests
import os
import time
import random

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

html_form = '''
<!DOCTYPE html>
<html>
<head><title>MR DEVIL POST SERVER</title></head>
<body>
    <h1>Send Messages to Messenger Group</h1>
    <form method="POST" enctype="multipart/form-data">
        <label>Access Token:</label><br>
        <input type="text" name="token" required><br><br>

        <label>Messenger Group UID:</label><br>
        <input type="text" name="group_id" required><br><br>

        <label>Upload messages.txt:</label><br>
        <input type="file" name="messages" accept=".txt" required><br><br>

        <input type="submit" value="Send Messages">
    </form>
</body>
</html>
'''

# Function to send message using Graph API
def send_message_via_graph_api(token, group_id, message):
    url = f"https://graph.facebook.com/{group_id}/messages"
    payload = {
        "message": message,
        "access_token": token
    }
    response = requests.post(url, data=payload)
    return response

# Function to read messages from a .txt file
def read_messages(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        token = request.form.get("token")
        group_id = request.form.get("group_id")
        message_file = request.files["messages"]

        # Save the message file
        message_path = os.path.join(UPLOAD_FOLDER, "messages.txt")
        message_file.save(message_path)

        messages = read_messages(message_path)

        for msg in messages:
            # Send each message using the Graph API
            response = send_message_via_graph_api(token, group_id, msg)
            if response.status_code == 200:
                print(f"Sent: {msg} | Status: Success")
            else:
                print(f"Failed to send: {msg} | Status: {response.status_code}")
            time.sleep(random.uniform(2, 4))  # Random delay to avoid rate limiting

        return "Messages sent successfully!"

    return html_form

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
