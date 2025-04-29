from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# HTML template to take user input (cookie)
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Token Generator</title>
</head>
<body>
    <h2>Enter Your Facebook Cookie</h2>
    <form method="POST">
        <textarea name="cookie" placeholder="Enter your Facebook cookie here" rows="5" cols="50"></textarea><br><br>
        <input type="submit" value="Generate Token">
    </form>

    {% if token %}
        <h3>Your Generated Token: </h3>
        <p>{{ token }}</p>
    {% endif %}
</body>
</html>
'''

def generate_token_from_cookie(user_cookie):
    url = f'https://graph.facebook.com/v14.0/me?access_token={user_cookie}'
    response = requests.get(url)

    if response.status_code == 200:
        access_token = response.json().get('access_token')
        return access_token if access_token else "Error: Token not found"
    else:
        return f"Error: {response.json().get('error', {}).get('message', 'Unknown error')}"

@app.route('/', methods=['GET', 'POST'])
def index():
    token = None
    if request.method == 'POST':
        user_cookie = request.form['cookie']
        if user_cookie:
            token = generate_token_from_cookie(user_cookie)
    return render_template_string(html_template, token=token)

if __name__ == '__main__':
    app.run(debug=True)
