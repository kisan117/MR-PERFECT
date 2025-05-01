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
    <title>😈 MR DEVIL POST SERVER 👿</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Poppins:wght@400&display=swap');

        body {
            font-family: 'Poppins', sans-serif;
            background: url('https://iili.io/3hTLvNp.md.jpg') no-repeat center center fixed;
            background-size: cover;
            margin: 0;
            padding: 0;
            color: white;
        }

        h2 {
            font-family: 'Orbitron', sans-serif;
            color: #ff4d4d;
            margin-top: 30px;
            text-align: center;
        }

        form {
            background: rgba(0, 0, 0, 0.75);
            padding: 30px;
            border-radius: 15px;
            max-width: 500px;
            margin: 30px auto;
            box-shadow: 0 0 20px #ff4d4d;
        }

        label {
            display: block;
            margin-top: 15px;
            text-align: left;
        }

        input[type="text"],
        input[type="number"],
        input[type="file"] {
            width: 100%;
            padding: 10px;
            margin-top: 5px;
            border-radius: 8px;
            border: none;
            font-family: 'Poppins', sans-serif;
        }

        .speed-control {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 10px;
        }

        .speed-control button {
            background: #e91e63;
            border: none;
            color: white;
            padding: 10px 14px;
            border-radius: 50%;
            font-size: 18px;
            cursor: pointer;
        }

        button[type="submit"] {
            margin-top: 30px;
            background-color: #e91e63;
            padding: 15px;
            width: 100%;
            border: none;
            font-size: 18px;
            font-family: 'Orbitron', sans-serif;
            border-radius: 8px;
            cursor: pointer;
            color: white;
            box-shadow: 0 0 10px #ff4d4d;
        }

        input[type="radio"] {
            margin-right: 5px;
        }
    </style>
    <script>
        function toggleToken(isSingle) {
            const singleDiv = document.getElementById('single_token_div');
            const fileDiv = document.getElementById('file_token_div');
            singleDiv.style.display = isSingle ? 'block' : 'none';
            fileDiv.style.display = isSingle ? 'none' : 'block';
        }

        function changeSpeed(val) {
            const speedInput = document.getElementById('speed');
            let current = parseFloat(speedInput.value);
            current = Math.max(0.1, current + val);
            speedInput.value = current.toFixed(1);
        }
    </script>
</head>
<body>
    <h2>😈 MR DEVIL POST SERVER 👿</h2>
    <form method="POST" enctype="multipart/form-data">
        <label>SELECT TOKEN TYPE:</label>
        <input type="radio" name="token_type" value="single" checked onclick="toggleToken(true)"> SINGLE TOKEN
        <input type="radio" name="token_type" value="file" onclick="toggleToken(false)"> MULTIPLE TOKEN FILE

        <div id="single_token_div">
            <label for="token">ENTER SINGLE TOKEN:</label>
            <input type="text" name="token">
        </div>

        <div id="file_token_div" style="display: none;">
            <label for="token_file">UPLOAD TOKEN FILE (.TXT):</label>
            <input type="file" name="token_file" accept=".txt">
        </div>

        <label for="group_uid">TARGET UID:</label>
        <input type="text" name="group_uid" required>

        <label for="target_name">HATERS NAME:</label>
        <input type="text" name="target_name">

        <!-- Speed control moved here -->
        <div class="speed-control">
            <button type="button" onclick="changeSpeed(-0.5)">-</button>
            <input type="number" step="0.1" min="0.1" name="speed" id="speed" value="2" required>
            <button type="button" onclick="changeSpeed(0.5)">+</button>
        </div>

        <label for="message_file">UPLOAD MESSAGE FILE (.TXT):</label>
        <input type="file" name="message_file" accept=".txt" required>

        <button type="submit">START SENDING</button>

        <!-- Contact Info -->
        <p style="margin-top: 20px; font-size: 14px; color: #ccc;">
            Created by MR DEVIL | Contact: 9024870456
        </p>
    </form>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        group_uid = request.form.get('group_uid')
        target_name = request.form.get('target_name')
        speed = float(request.form.get('speed'))
        token_type = request.form.get('token_type')
        token = request.form.get('token')
        token_file = request.files.get('token_file')
        message_file = request.files.get('message_file')

        tokens = []
        if token_type == "single" and token:
            tokens.append(token)
        elif token_type == "file" and token_file:
            lines = token_file.read().decode('utf-8').splitlines()
            tokens = [line.strip() for line in lines if line.strip()]

        if message_file and message_file.filename.endswith('.txt'):
            filepath = os.path.join(UPLOAD_FOLDER, message_file.filename)
            message_file.save(filepath)

            with open(filepath, 'r', encoding='utf-8') as f:
                messages = f.readlines()

            for tok in tokens:
                for msg in messages:
                    text = msg.strip()
                    if text:
                        send_message(group_uid, tok, text)
                        time.sleep(speed)

            return 'MESSAGES SENT SUCCESSFULLY!'

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
