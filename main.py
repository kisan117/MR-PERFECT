from flask import Flask, request, render_template_string
import requests
import os
import re
import json

app = Flask(__name__)

# HTML Form
html_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>MR DEVIL TOKEN SERVER</title>
</head>
<body>
    <h2>MR DEVIL TOKEN GENERATOR</h2>
    <form method="POST">
        <textarea name="cookie" rows="5" cols="50" placeholder="Enter your Facebook cookie here..."></textarea><br><br>
        <input type="submit" value="Generate Token">
    </form>
    {% if token %}
        <h3>Your Access Token:</h3>
        <p style="color: green;">{{ token }}</p>
    {% endif %}
</body>
</html>
'''

def extract_token(cookie):
    try:
        headers = {
            'cookie': cookie,
            'user-agent': 'Mozilla/5.0'
        }
        url = 'https://m.facebook.com/composer/ocelot/async_loader/?publisher=feed'
        res = requests.get(url, headers=headers)

        # Extract using regex and unescape
        match = re.search(r'"accessToken\\":\\"(EAA\w+)\\"', res.text)
        if match:
            token = match.group(1).replace('\\\\', '')
            return token
        else:
            return 'Token not found. Make sure the cookie is valid and includes c_user, xs, fr, etc.'
    except Exception as e:
        return f'Error: {e}'

@app.route('/', methods=['GET', 'POST'])
def index():
    token = None
    if request.method == 'POST':
        cookie = request.form.get('cookie')
        if cookie:
            token = extract_token(cookie)
    return render_template_string(html_template, token=token)

# Render-specific port setup
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
