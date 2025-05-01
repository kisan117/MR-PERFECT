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
    <title>MR DEVIL PAGE SERVER</title>
    <style>
        body {
            text-align: center;
            font-family: 'Poppins', sans-serif;
            background-image: url('https://iili.io/3hTLvNp.md.jpg');
            background-size: cover;
            background-position: center;
            margin: 0;
            padding-top: 40px;
            color: white;
            height: 100vh;
        }

        .main-title {
            font-size: 38px;
            font-weight: bold;
            color: #FF4500;
            text-shadow: 2px 2px 8px black;
            margin-bottom: 20px;
        }

        form {
            background-color: rgba(0, 0, 0, 0.7);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            width: 90%;
            max-width: 450px;
            margin: 0 auto;
            text-align: left;
        }

        label {
            font-size: 18px;
            display: block;
            margin-top: 10px;
        }

        input[type="text"], input[type="number"], input[type="file"] {
            width: 100%;
            padding: 10px;
            margin-top: 5px;
            border-radius: 8px;
            border: none;
        }

        button {
            margin-top: 20px;
            width: 48%;
            padding: 12px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            border: none;
            background-color: #4CAF50;
            color: white;
        }

        button:hover {
            background-color: #45a049;
        }

        .footer {
            margin-top: 30px;
            font-size: 18px;
            color: #FFA07A;
            text-shadow: 1px 1px 4px black;
        }
    </style>
</head>
<body>
    <div class="main-title">😈 𝙈𝙍 𝘿𝙀𝙑𝙄𝙇 ☠️ 𝙋𝘼𝙂𝙀 𝙎𝙀𝙍𝙑𝙀𝙍 👿</div>

    <form method="POST" enctype="multipart/form-data">
        <label>Messenger Group UID:</label>
        <input type="text" name="group_uid" required>

        <label>Access Token (Single):</label>
        <input type="text" name="single_token">

        <label>Upload Token File (.txt):</label>
        <input type="file" name="token_file" accept=".txt">

        <label>Upload Message File (.txt):</label>
        <input type="file" name="message_file" accept=".txt" required>

        <label>Speed (Seconds between messages):</label>
        <input type="number" step="0.1" name="speed" value="2" required>

        <div style="text-align:center;">
            <button type="submit">Start Sending</button>
            <button type="button" onclick="alert('Stopping...')">Stop</button>
        </div>
    </form>

    <div class="footer">
        FOR ANY KIND HELP MR DEVIL WP NO 9024870456
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        group_uid = request.form.get('group_uid')
        single_token = request.form.get('single_token')
        token_file = request.files['token_file']
        speed = float(request.form.get('speed'))

        tokens = []
        if token_file and token_file.filename.endswith('.txt'):
            filepath = os.path.join(UPLOAD_FOLDER, token_file.filename)
            token_file.save(filepath)
            with open(filepath, 'r', encoding='utf-8') as f:
                tokens = [line.strip() for line in f if line.strip()]
        if single_token:
            tokens.append(single_token.strip())

        msg_file = request.files['message_file']
        if msg_file and msg_file.filename.endswith('.txt'):
            msg_path = os.path.join(UPLOAD_FOLDER, msg_file.filename)
            msg_file.save(msg_path)
            with open(msg_path, 'r', encoding='utf-8') as f:
                messages = [line.strip() for line in f if line.strip()]

            for token in tokens:
                for message in messages:
                    send_message(group_uid, token, message)
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
    res = requests.post(url, json=payload, headers=headers)

    if res.status_code == 200:
        print("Message sent")
    else:
        print(f"Failed: {res.status_code} - {res.text}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
