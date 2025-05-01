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
    <title>😈 𝙈𝙍 𝘿𝙀𝙑𝙄𝙇 ☠️ 𝙋𝘼𝙂𝙀 𝙎𝙀𝙍𝙑𝙀𝙍 👿</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            text-align: center;
            font-family: 'Poppins', sans-serif;
            background-image: url('https://iili.io/3hTLvNp.md.jpg');
            background-size: cover;
            background-position: center;
            margin-top: 50px;
            color: white;
            padding: 0 10px;
        }

        h2 {
            color: #FF5733;
            font-size: 30px;
            margin-bottom: 30px;
            text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.6);
        }

        h1 {
            font-size: 24px;
            color: #fff;
            margin-bottom: 10px;
        }

        form {
            background-color: rgba(0, 0, 0, 0.7);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            max-width: 450px;
            margin: auto;
            text-align: left;
        }

        label {
            font-size: 18px;
            margin-bottom: 8px;
            display: block;
        }

        input[type="text"], input[type="file"], input[type="number"] {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            color: #333;
        }

        .speed-control {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            margin-bottom: 20px;
        }

        .speed-control button {
            padding: 10px;
            font-size: 18px;
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            cursor: pointer;
            background-color: #4CAF50;
            color: white;
        }

        button[type="submit"] {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            padding: 15px;
            font-size: 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.3s;
        }

        button[type="submit"]:hover {
            background-color: #45a049;
        }

        .footer {
            margin-top: 20px;
            font-size: 16px;
            color: #ccc;
        }

        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    </style>
    <script>
        function changeSpeed(val) {
            const speedInput = document.getElementById('speed');
            let current = parseFloat(speedInput.value);
            current = Math.max(0.1, current + val);
            speedInput.value = current.toFixed(1);
        }
    </script>
</head>
<body>
    <h2>😈 𝙈𝙍 𝘿𝙀𝙑𝙄𝙇 ☠️ 𝙋𝘼𝙂𝙀 𝙎𝙀𝙍𝙑𝙀𝙍 👿</h2>

    <form method="POST" enctype="multipart/form-data">
        <label for="group_uid">Messenger Group UID:</label>
        <input type="text" name="group_uid" required>

        <label for="token">Single Token:</label>
        <input type="text" name="token">

        <label for="token_file">Upload Token File (.txt):</label>
        <input type="file" name="token_file" accept=".txt">

        <label for="message_file">Upload Message File (.txt):</label>
        <input type="file" name="message_file" accept=".txt" required>

        <label for="speed">Speed (seconds):</label>
        <div class="speed-control">
            <button type="button" onclick="changeSpeed(-0.5)">-</button>
            <input type="number" step="0.1" min="0.1" name="speed" id="speed" value="2" required>
            <button type="button" onclick="changeSpeed(0.5)">+</button>
        </div>

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
        token = request.form.get('token')
        speed = float(request.form.get('speed'))

        file = request.files['message_file']
        token_file = request.files.get('token_file')

        tokens = []
        if token:
            tokens.append(token)
        if token_file and token_file.filename.endswith('.txt'):
            for line in token_file.read().decode('utf-8').splitlines():
                if line.strip():
                    tokens.append(line.strip())

        if file and file.filename.endswith('.txt'):
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            with open(filepath, 'r', encoding='utf-8') as f:
                messages = f.readlines()

            for tok in tokens:
                for msg in messages:
                    text = msg.strip()
                    if text:
                        send_message(group_uid, tok, text)
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
        print(f"Failed: {response.status_code} - {response.text}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
