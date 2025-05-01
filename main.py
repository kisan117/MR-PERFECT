from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Facebook Reaction Tool</title>
    <style>
        body {
            font-family: Arial;
            text-align: center;
            background: url('https://i.ibb.co/r2LjfV3x/2d8b98aa48e24c185694c9f04989eed8.jpg') no-repeat center center fixed;
            background-size: cover;
            color: #000;
        }
        .box {
            background: rgba(255,255,255,0.9);
            padding: 20px;
            margin: 100px auto;
            border-radius: 10px;
            width: 90%;
            max-width: 400px;
        }
        input, select, button {
            padding: 10px;
            width: 90%;
            margin: 10px 0;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        button {
            background: #28a745;
            color: white;
            border: none;
        }
    </style>
</head>
<body>
    <div class="box">
        <h2>Facebook Reaction Tool</h2>
        <form method="POST">
            <input type="text" name="access_token" placeholder="Access Token" required><br>
            <input type="text" name="post_id" placeholder="Post ID" required><br>
            <select name="reaction_type" required>
                <option value="LIKE">LIKE</option>
                <option value="LOVE">LOVE</option>
                <option value="HAHA">HAHA</option>
                <option value="WOW">WOW</option>
                <option value="SAD">SAD</option>
                <option value="ANGRY">ANGRY</option>
            </select><br>
            <button type="submit">Send Reaction</button>
        </form>
        {% if message %}
            <p style="color: green;">{{ message }}</p>
        {% endif %}
        {% if error %}
            <p style="color: red;">{{ error }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        access_token = request.form['access_token']
        post_id = request.form['post_id']
        reaction_type = request.form['reaction_type']

        # Graph API v12.0 Endpoint
        graph_url = f"https://graph.facebook.com/v12.0/{post_id}/reactions"
        payload = {
            "type": reaction_type,
            "access_token": access_token
        }

        try:
            # Sending the POST request to the API
            response = requests.post(graph_url, data=payload)
            result = response.json()

            if response.status_code == 200:
                return render_template_string(HTML_TEMPLATE, message=f"{reaction_type} reaction sent successfully!")
            else:
                error = result.get("error", {}).get("message", "Something went wrong.")
                return render_template_string(HTML_TEMPLATE, error=f"Error: {error}")
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, error=f"Exception occurred: {str(e)}")

    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
