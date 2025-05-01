from flask import Flask, request
import requests
import random
import time

app = Flask(__name__)

html_form = '''
<!DOCTYPE html>
<html>
<head>
    <title>MR DEVIL MSG SERVER</title>
</head>
<body>
    <h1>Send Message to Messenger Group</h1>
    <form method="POST" enctype="multipart/form-data">
        <label>Access Token:</label><br>
        <input type="text" name="token" required><br><br>

        <label>Messenger Group UID:</label><br>
        <input type="text" name="group_id" required><br><br>

        <label>Upload .txt File with Messages:</label><br>
        <input type="file" name="messages" accept=".txt" required><br><br>

        <input type="submit" value="Send Messages">
    </form>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        token = request.form.get("token")
        group_id = request.form.get("group_id")
        file = request.files["messages"]
        messages = [line.strip() for line in file.read().decode().splitlines() if line.strip()]

        for msg in messages:
            payload = {
                "message": msg,
                "access_token": token
            }
            url = f"https://graph.facebook.com/{group_id}/messages"
            response = requests.post(url, data=payload)
            print(f"Sent: {msg} | Status: {response.status_code}")
            time.sleep(random.uniform(1, 3))  # Delay between messages

        return "Messages sent successfully!"

    return html_form

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
