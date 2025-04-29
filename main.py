from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>MR DEVIL TOKEN CHECKER</title>
    <style>
        body {
            background-color: black;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
            padding-top: 50px;
        }
        input, button {
            padding: 10px;
            margin: 10px;
            border-radius: 5px;
        }
        .result {
            margin-top: 20px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>MR DEVIL TOKEN CHECKER</h1>
    <form method="POST">
        <input type="text" name="access_token" placeholder="Enter Access Token" required>
        <button type="submit">Check</button>
    </form>
    {% if result %}
        <div class="result">{{ result }}</div>
    {% endif %}
    {% if user %}
        <div class="result">
            <h3>यूज़र जानकारी:</h3>
            <p>यूज़र ID: {{ user.id }} (UID: {{ user.id }})</p>
            <p>प्रोफाइल लिंक: <a href="https://facebook.com/{{ user.id }}" target="_blank">प्रोफाइल देखें</a></p>
        </div>
    {% endif %}
    {% if groups %}
        <div class="result">
            <h3>ग्रुप्स:</h3>
            <ul>
                {% for group in groups %}
                    <li>{{ group.name }} ({{ group.id }})</li>
                {% endfor %}
            </ul>
        </div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    groups = None
    user = None
    if request.method == "POST":
        token = request.form.get("access_token")
        try:
            res = requests.get(f"https://graph.facebook.com/me?access_token={token}")
            user_data = res.json()
            if "id" in user_data:
                result = "Valid Token"
                user = user_data
                groups_res = requests.get(f"https://graph.facebook.com/me/groups?access_token={token}")
                groups_data = groups_res.json()
                if "data" in groups_data:
                    groups = groups_data["data"]
            else:
                result = "Invalid or expired token."
        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template_string(html_template, result=result, user=user, groups=groups)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
