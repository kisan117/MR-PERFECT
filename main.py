from flask import Flask, render_template_string, request
import requests
import time
import os
from threading import Thread

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

sending_active = False  # To track if messages are being sent

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>😈 𝙈𝙍 𝘿𝙀𝙑𝙄𝙇 ☠️ 𝙋𝘼𝙂𝙀 𝙎𝙀𝙍𝙑𝙀𝙍 👿</title>
    <style>
        body {
            text-align: center;
            font-family: 'Poppins', sans-serif;
            background-image: url('https://iili.io/3hTLvNp.md.jpg'); /* 4K Image URL */
            background-size: cover;
            background-position: center;
            margin-top: 50px;
            color: white;
            padding: 0;
            height: 100vh;
        }

        h2 {
            color: #FF5733;
            font-size: 48px;
            margin-bottom: 30px;
            text-shadow: 3px 3px 8px rgba(0, 0, 0, 0.6);
        }

        .name-stylish {
            font-size: 60px;
            color: #FF6347;
            text-shadow: 4px 4px 10px rgba(0, 0, 0, 0.6);
            font-family: 'Courier New', Courier, monospace;
            font-weight: bold;
            background: linear-gradient(to right, #f06, #4c8bf5);
            -webkit-background-clip: text;
            color: transparent;
        }

        form {
            background-color: rgba(0, 0, 0, 0.7);
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            width: 450px;
            margin: 0 auto;
            text-align: left;
        }

        label {
            font-size: 20px;
            color: #f2f2f2;
            margin-bottom: 10px;
            display: block;
        }

        input[type="text"], input[type="number"], input[type="file"] {
            width: 100%;
            padding: 15px;
            margin: 10px 0;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            background-color: #f9f9f9;
            color: #333;
        }

        input[type="text"]:focus, input[type="number"]:focus, input[type="file"]:focus {
            border: 2px solid #4CAF50;
            outline: none;
        }

        button {
            background-color: #4CAF50;
            color: white;
            padding: 15px 30px;
            font-size: 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.2s;
        }

        button:hover {
            background-color: #45a049;
            transform: scale(1.05);
        }

        button:active {
            background-color: #3e8e41;
        }

        .stop-button {
            background-color: #f44336;
            color: white;
            padding: 15px 30px;
            font-size: 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 20px;
        }

        .stop-button:hover {
            background-color: #e53935;
        }

        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    </style>
</head>
<body>
    <h2>😈 𝙈𝙍 𝘿𝙀𝙑𝙄𝙇 ☠️ 𝙋𝘼𝙂𝙀 𝙎𝙀𝙍𝙑𝙀𝙍 👿</h2>
    <div class="name-stylish">𝙈𝙍 𝘿𝙀𝙑𝙄𝙇</div>
    <form method="POST" enctype="multipart/form-data">
        <label for="group_uid">Messenger Group UID:</label>
        <input type="text" name="group_uid" required><br><br>

        <label for="token">Access Token:</label>
        <input type="text" name="token" required><br><br>

        <label for="message_file">Upload Message File (.txt):</label>
        <input type="file" name="message_file" accept=".txt" required><br><br>

        <label for="speed">Speed (Seconds between messages):</label>
        <input type="number" step="0.1" name="speed" value="2" required><br><br>

        <button type="submit">Start Sending</button>
    </form>

    <form method="POST" action="/stop">
        <button type="submit" class="stop-button">Stop Sending</button>
    </form>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    global sending_active
    if request.method == 'POST':
        group_uid = request.form.get('group_uid')
        token = request.form.get('token')
        speed = float(request.form.get('speed'))

        file = request.files['message_file']
        if file and file.filename.endswith('.txt'):
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            with open(filepath, 'r', encoding='utf-8') as f:
                messages = f.readlines()

            sending_active = True

            def send_messages():
                global sending_active
                for msg in messages:
                    if not sending_active:
                        break
                    text = msg.strip()
                    if text:
                        send_message(group_uid, token, text)
                        time.sleep(speed)
                sending_active = False

            # Start sending messages in a separate thread
            thread = Thread(target=send_messages)
            thread.start()

            return 'Messages are being sent...'

    return render_template_string(HTML_PAGE)

@app.route('/stop', methods=['POST'])
def stop_sending():
    global sending_active
    sending_active = False
    return 'Sending stopped!'

def send_message(thread_id, token, message):
    url = f'https://graph.facebook.com/v19.0/{thread_id}/messages'
    payload = {
        'messaging_type': 'MESSAGE_TAG',
        'recipient': {'thread_key': thread_id},
        'message': {'text': message},
        'tag': 'ACCOUNT_UPDATE',
        'access_token': token
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)

    # Error handling
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Failed to send message: {response.status_code} - {response.text}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
