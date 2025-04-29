from flask import Flask, request, render_template_string
import requests
import os
import re

app = Flask(__name__)

# HTML Page
html_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>MR DEVIL TOKEN GENERATOR</title>
    <style>
        body { font-family: Arial, sans-serif; background: #111; color: white; text-align: center; padding-top: 50px; }
        textarea { width: 80%; height: 100px; border-radius: 8px; }
        input[type="submit"] { padding: 10px 20px; border: none; background: green; color: white; border-radius: 5px; margin-top: 10px; }
        .token { margin-top: 20px; word-break: break-all; background: #222; padding: 10px; border-radius: 8px; }
    </style>
</head>
<body>
    <h1>MR DEVIL TOKEN SERVER</h1>
    <form method="POST">
        <textarea name="cookie" placeholder="Enter your Facebook cookie here..." required></textarea><br><br>
        <input type="submit" value="Generate Token">
    </form>
    {% if token %}
        <div class="token">
            <h3>Your Token:</h3>
            <p>{{ token }}</p>
        </div>
    {% endif %}
</body>
</html>
'''

# Extract Token function
def extract_token(cookie):
    try:
        headers = {
            'cookie': cookie,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36'
        }
        url = 'https://m.facebook.com/composer/ocelot/async_loader/?publisher=feed'
        response = requests.get(url, headers=headers)
        
        # Debugging: Print the full response text to check what Facebook returns
        print("Response Text:", response.text)

        # Check if session is valid or cookie is expired
        if "for (;;);" in response.text or "login" in response.url:
            return 'Session expired or invalid cookie!'

        # Extract token using regex
        match = re.search(r'"accessToken":"(EAA\w+)"', response.text)
        if match:
            token = match.group(1)
            return token
        else:
            return 'Token not found. Make sure the cookie is fresh and correct.'
    except Exception as e:
        return f'Error: {str(e)}'

# Flask Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    token = None
    if request.method == 'POST':
        cookie = request.form.get('cookie')
        print(f"Received Cookie: {cookie}")  # Debugging: Print the received cookie
        if cookie:
            token = extract_token(cookie)
    return render_template_string(html_template, token=token)

# Main
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
