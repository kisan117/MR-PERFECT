from flask import Flask, render_template_string, request
import requests
import time
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>MR DEVIL POST SERVER</title>
</head>
<body style="text-align:center; font-family:sans-serif;">
    <h2>MR DEVIL MESSENGER POST SERVER</h2>
    <form method="POST" enctype="multipart/form-data">
        <label>Messenger Group UID:</label><br>
        <input type="text" name="group_uid" required><br><br>

        <label>Access Token:</label><br>
        <input type="text" name="token" required><br><br>

        <label>Upload Message File (.txt):</label><br>
        <input type="file" name="message_file" accept=".txt" required><br><br>

        <label>Speed (Seconds between messages):</label><br>
        <input type="number" step="0.1" name="speed" value="2" required><br><br>

        <button type="submit">Start Sending</button>
    </form>
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
        if file and file.filename.endswith('.txt'):
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            with open(filepath, 'r', encoding='utf-8') as f:
                messages = f.readlines()

            for msg in messages:
                text = msg.strip()
                if text:
                    send_message(group_uid, token, text)
                    time.sleep(speed)

            return 'Messages sent successfully!'

    return render_template_string(HTML_PAGE)

def send_message(thread_id, token, message):
    url = 'https://graph.facebook.com/v19.0/me/messages'
    payload = {
        'messaging_type': 'MESSAGE_TAG',
        'recipient': {'thread_key': thread_id},
        'message': {'text': message},
        'tag': 'ACCOUNT_UPDATE',
        'access_token': token
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
