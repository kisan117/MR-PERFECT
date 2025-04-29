from flask import Flask, request, render_template_string
import requests
import re
import os

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html>
<head>
    <title>MR DEVIL TOKEN TOOL</title>
    <style>
        body {
            background: #0f0f0f url('https://i.ibb.co/6RK46Spg/fcca220ee657a7b387a986ce99887b82.jpg') no-repeat center center fixed;
            background-size: cover;
            font-family: Arial, sans-serif;
            color: white;
            text-align: center;
            padding-top: 50px;
        }
        .box {
            background: rgba(0, 0, 0, 0.7);
            padding: 30px;
            border-radius: 10px;
            display: inline-block;
        }
        textarea {
            width: 90%%;
            height: 100px;
            padding: 10px;
            border-radius: 5px;
            border: none;
        }
        input[type=submit] {
            padding: 10px 20px;
            background: green;
            color: white;
            border: none;
            border-radius: 5px;
            margin-top: 10px;
            cursor: pointer;
        }
        .result {
            margin-top: 20px;
            background: #222;
            padding: 10px;
            border-radius: 8px;
            word-break: break-all;
        }
    </style>
</head>
<body>
    <div class="box">
        <h1>MR DEVIL COOKIE TO TOKEN</h1>
        <form method="POST">
            <textarea name="cookie" placeholder="Paste your Facebook cookie here..." required></textarea><br>
            <input type="submit" value="Get Token">
        </form>
        {% if token %}
        <div class="result">
            <h3>Access Token:</h3>
            <p>{{ token }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

def get_token(cookie):
    try:
        headers = {
            'cookie': cookie,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36'
        }
        url = 'https://m.facebook.com/composer/ocelot/async_loader/?publisher=feed'
        response = requests.get(url, headers=headers)

        match = re.search(r'"accessToken\\":\\"(EAA\w+)\\"', response.text)
        if match:
            return match.group(1)
        return "Token not found or cookie invalid!"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    token = None
    if request.method == "POST":
        cookie = request.form.get("cookie")
        if cookie:
            token = get_token(cookie)
    return render_template_string(html, token=token)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
