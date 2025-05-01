from flask import Flask, request, render_template_string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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
</head>
<body>
    <h2>Messenger Group Message Sender</h2>
    <form method="POST" enctype="multipart/form-data">
        <label>Token (c_user|xs):</label><br>
        <input type="text" name="token" required><br><br>

        <label>Messenger Group UID:</label><br>
        <input type="text" name="group_uid" required><br><br>

        <label>Speed (delay in seconds):</label><br>
        <input type="number" name="speed" step="0.5" required><br><br>

        <label>Message File (.txt):</label><br>
        <input type="file" name="message_file" accept=".txt" required><br><br>

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

        filepath = os.path.join(UPLOAD_FOLDER, message_file.filename)
        message_file.save(filepath)

        with open(filepath, 'r', encoding='utf-8') as f:
            messages = f.read().splitlines()

        send_messages_to_group(token, group_uid, delay, messages)
        return "Messages sent successfully."

    return render_template_string(HTML_TEMPLATE)

def send_messages_to_group(token, group_uid, delay, messages):
    user_id, xs = token.split('|')

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
    app.run(debug=True)
