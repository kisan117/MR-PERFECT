from flask import Flask, request, render_template_string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import time
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>MR DEVIL MESSENGER BOT</title>
    <style>
        body {
            background-color: #111;
            color: #0f0;
            font-family: monospace;
            padding: 20px;
        }
        h1, h2 {
            color: #0ff;
            text-align: center;
        }
        form {
            max-width: 500px;
            margin: auto;
            padding: 20px;
            background: #222;
            border: 2px solid #0f0;
            border-radius: 10px;
        }
        label {
            display: block;
            margin-top: 10px;
            font-size: 18px;
        }
        input, button {
            width: 100%;
            padding: 8px;
            margin-top: 5px;
            font-size: 16px;
            background-color: #000;
            color: #0f0;
            border: 1px solid #0f0;
            border-radius: 5px;
        }
        button:hover {
            background-color: #0f0;
            color: #000;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>MR DEVIL POST SERVER</h1>
    <h2>Messenger Group Message Sender</h2>
    <form method="POST" enctype="multipart/form-data">
        <label>Token (c_user|xs):</label>
        <input type="text" name="token" required>

        <label>Messenger Group UID:</label>
        <input type="text" name="group_uid" required>

        <label>Speed (delay in seconds):</label>
        <input type="number" name="speed" step="0.5" required>

        <label>Message File (.txt):</label>
        <input type="file" name="message_file" accept=".txt" required>

        <button type="submit">Send Messages</button>
    </form>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        token = request.form['token']
        group_uid = request.form['group_uid']
        delay = float(request.form['speed'])
        message_file = request.files['message_file']

        if not token or not group_uid or not message_file:
            return "Please fill in all fields."

        # Token Split and Graph API Check
        if '|' not in token:
            return "Invalid token format. Use c_user|xs."

        user_id, xs = token.split('|')

        if not verify_token_graph_api(user_id):
            return "Invalid or expired Facebook token."

        filepath = os.path.join(UPLOAD_FOLDER, message_file.filename)
        message_file.save(filepath)

        with open(filepath, 'r', encoding='utf-8') as f:
            messages = f.read().splitlines()

        send_messages_to_group(user_id, xs, group_uid, delay, messages)
        return "Messages sent successfully."

    return render_template_string(HTML_TEMPLATE)

def verify_token_graph_api(user_id):
    try:
        url = f"https://graph.facebook.com/{user_id}"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }
        response = requests.get(url, headers=headers)
        return response.status_code == 200
    except Exception as e:
        print("Graph API error:", e)
        return False

def send_messages_to_group(user_id, xs, group_uid, delay, messages):
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    driver.get('https://mbasic.facebook.com')
    driver.add_cookie({'name': 'c_user', 'value': user_id, 'domain': '.facebook.com'})
    driver.add_cookie({'name': 'xs', 'value': xs, 'domain': '.facebook.com'})
    driver.get(f'https://mbasic.facebook.com/messages/thread/{group_uid}')

    for msg in messages:
        try:
            textarea = driver.find_element(By.NAME, 'body')
            textarea.send_keys(msg)
            driver.find_element(By.NAME, 'Send').click()
            time.sleep(delay)
        except Exception as e:
            print("Error sending:", msg, e)

    driver.quit()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
