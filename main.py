from flask import Flask, render_template_string, request
import requests
import time
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>𝙈𝙍 𝘿𝙀𝙑𝙄𝙇 𝙋𝘼𝙂𝙀 𝙎𝙀𝙍𝙑𝙀𝙍</title>
    <style>
        body {
            text-align: center;
            font-family: 'Poppins', sans-serif;
            background-image: url('https://iili.io/3hTLvNp.md.jpg');
            background-size: cover;
            background-position: center;
            color: white;
            padding: 20px;
            margin: 0;
        }

        .main-title {
            font-size: 7vw;
            font-weight: bold;
            margin: 30px 0;
            text-shadow: 2px 2px 10px black;
            color: #FF5733;
        }

        form {
            background-color: rgba(0, 0, 0, 0.7);
            padding: 30px;
            border-radius: 15px;
            max-width: 500px;
            margin: 0 auto;
        }

        label, input, button {
            font-size: 4vw;
            display: block;
            width: 100%;
            margin: 10px 0;
        }

        input, button {
            padding: 10px;
            border-radius: 8px;
            border: none;
        }

        button {
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
        }

        button:hover {
            background-color: #45a049;
        }

        .footer {
            margin-top: 30px;
            font-size: 4vw;
            color: #f0f0f0;
        }

        @media (min-width: 600px) {
            .main-title {
                font-size: 36px;
            }
            label, input, button, .footer {
                font-size: 18px;
            }
        }
    </style>
</head>
<body>
    <div class="main-title">𝙈𝙍 𝘿𝙀𝙑𝙄𝙇 𝙋𝘼𝙂𝙀 𝙎𝙀𝙍𝙑𝙀𝙍</div>

    <form method="POST" enctype="multipart/form-data">
        <label for="group_uid">Messenger Group UID:</label>
        <input type="text" name="group_uid" required>

        <label for="token">Single Token:</label>
        <input type="text" name="token">

        <label for="token_file">Upload Token File (.txt):</label>
        <input type="file" name="token_file" accept=".txt">

        <label for="message_file">Upload Message File (.txt):</label>
        <input type="file" name="message_file" accept=".txt" required>

        <label for="speed">Speed (Seconds between messages):</label>
        <input type="number" step="0.1" name="speed" value="2" required>

        <button type="submit">Start Sending</button>
    </form>

    <div class="footer">FOR ANY KIND HELP MR DEVIL WP NO 9024870456</div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        group_uid = request.form.get('group_uid')
        speed = float(request.form.get('speed'))
        message_file = request.files['message_file']
        token = request.form.get('token')
        token_file = request.files.get('token_file')

        if message_file and message_file.filename.endswith('.txt'):
            message_path = os.path.join(UPLOAD_FOLDER, message_file.filename)
            message_file.save(message_path)

            with open(message_path, 'r', encoding='utf-8') as f:
                messages = [line.strip() for line in f if line.strip()]

            tokens = []
            if token:
                tokens.append(token)
            elif token_file and token_file.filename.endswith('.txt'):
                token_path = os.path.join(UPLOAD_FOLDER, token_file.filename)
                token_file.save(token_path)
                with open(token_path, 'r', encoding='utf-8') as tf:
                    tokens = [line.strip() for line in tf if line.strip()]

            for msg in messages:
                for tk in tokens:
                    send_message(group_uid, tk, msg)
                    time.sleep(speed)

            return 'Messages sent successfully!'
    return render_template_string(HTML_PAGE)

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

    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Failed to send message: {response.status_code} - {response.text}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
