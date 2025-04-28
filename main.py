import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from flask import Flask, render_template_string, request
from threading import Thread
import os

app = Flask(__name__)

stop_flag = False

# Setup Chrome Options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = "/usr/bin/google-chrome"  # Chrome binary path for Render

# Setup WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open WhatsApp Web
driver.get("https://web.whatsapp.com/")
print("WhatsApp QR Code scan kar lo...")
time.sleep(20)  # User ko scan karne ka time mile

# Function to send messages
def send_messages(contact_name, message_text, delay):
    global stop_flag
    try:
        while not stop_flag:
            # Search contact/group
            search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            search_box.clear()
            search_box.send_keys(contact_name)
            search_box.send_keys(Keys.ENTER)
            time.sleep(2)

            # Send message
            message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
            message_box.send_keys(message_text)
            message_box.send_keys(Keys.ENTER)
            print(f"Message sent to {contact_name}: {message_text}")

            time.sleep(delay)
    except Exception as e:
        print(f"Error: {str(e)}")

# Home page
@app.route("/", methods=["GET", "POST"])
def index():
    global stop_flag
    if request.method == "POST":
        if request.form.get("action") == "start":
            stop_flag = False
            contact_name = request.form["target"]
            message_text = request.form["message"]
            delay = int(request.form.get("delay", 5))  # Default delay = 5 seconds
            thread = Thread(target=send_messages, args=(contact_name, message_text, delay))
            thread.start()
            return "Messages sending started!"
        elif request.form.get("action") == "stop":
            stop_flag = True
            return "Messages sending stopped!"
    
    return render_template_string('''
    <h1>MR DEVIL WhatsApp Bot</h1>
    <form method="post">
        <input type="text" name="target" placeholder="Contact ya Group Name" required><br><br>
        <input type="text" name="message" placeholder="Message Text" required><br><br>
        <input type="number" name="delay" placeholder="Delay (seconds)" value="5"><br><br>
        <button type="submit" name="action" value="start">Start Sending</button>
        <button type="submit" name="action" value="stop">Stop Sending</button>
    </form>
    ''')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
