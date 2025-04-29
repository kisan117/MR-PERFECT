from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)

# Simple HTML form
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
        <p>{{ token }}</p>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    token = None
    if request.method == 'POST':
        cookie = request.form.get('cookie')
        if cookie:
            headers = {
                'cookie': cookie,
                'user-agent': 'Mozilla/5.0'
            }
            try:
                res = requests.get('https://business.facebook.com/business_locations', headers=headers)
                token = res.text.split('EAAG')[1].split('"')[0]
                token = 'EAAG' + token
            except:
                token = 'Invalid cookie or token not found!'
    return render_template_string(html_template, token=token)

# Required for Render deployment
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
