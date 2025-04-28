import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from flask import Flask, render_template_string, request
from threading import Thread

# Flask app initialization
app = Flask(__name__)

# Global variable to control message sending
stop_flag = False

# Set up Chrome options for headless mode (optional)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run browser in background (optional)
chrome_options.add_argument("--disable-gpu")

# Set up the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open WhatsApp Web
driver.get("https://web.whatsapp.com/")

# Wait for QR Code scan
print("Please scan the QR code from WhatsApp Web...")
time.sleep(15)  # Adjust this if necessary to give time for scanning the QR code

# Define the target contact/group
target = "MR DEVIL"  # Contact or group name in WhatsApp

# Function to read messages from file
def read_messages_from_file(filename):
    with open(filename, "r") as file:
        messages = file.readlines()
    return [msg.strip() for msg in messages]

# Function to read delay time from SPEED.txt file
def get_delay_from_file():
    try:
        with open("SPEED.txt", "r") as file:
            delay = int(file.read().strip())  # Read and convert the delay to integer
            return delay
    except FileNotFoundError:
        print("SPEED.txt file not found! Using default delay of 5 seconds.")
        return 5  # Default delay if the file is not found
    except ValueError:
        print("Invalid value in SPEED.txt! Using default delay of 5 seconds.")
        return 5  # Default delay if the value is not valid

# Function to send message with delay and loop for repeated messages
def send_message(contact_name, messages, delay):
    global stop_flag  # Use the global stop_flag
    try:
        while True:  # Infinite loop to repeat sending messages
            if stop_flag:  # If stop flag is set to True, exit the loop
                print("Message sending stopped.")
                break

            for message in messages:  # Loop through each message
                # Search for the contact/group
                search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
                search_box.clear()
                search_box.send_keys(contact_name)
                search_box.send_keys(Keys.ENTER)
                time.sleep(2)

                # Find the message box and send the message
                message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="1"]')
                message_box.send_keys(message)
                message_box.send_keys(Keys.ENTER)
                print(f"Message sent to {contact_name}: {message}")

                # Wait for the specified delay before sending the next message
                time.sleep(delay)  # Delay between messages

    except Exception as e:
        print(f"Error while sending message: {str(e)}")

# Flask route to control message sending
@app.route("/", methods=["GET", "POST"])
def index():
    global stop_flag  # Use the global stop flag to stop messages
    if request.method == "POST":
        action = request.form.get('action')
        if action == "stop":
            stop_flag = True  # Set stop flag to True to stop message sending
            return "Message sending has been stopped."
        elif action == "start":
            stop_flag = False  # Set stop flag to False to start sending messages
            messages = read_messages_from_file("messages.txt")  # Replace with your actual file path
            delay = get_delay_from_file()  # Get the delay from SPEED.txt
            thread = Thread(target=send_message, args=(target, messages, delay))  # Use delay from file
            thread.start()
            return "Message sending has started."
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>WhatsApp Message Bot</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f0f0; text-align: center; }
        form {
            background: white;
            padding: 20px;
            margin: 30px auto;
            width: 90%;
            max-width: 400px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px grey;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
        }
        button {
            background: green;
            color: white;
            border: none;
            cursor: pointer;
            border-radius: 5px;
        }
        .stop-btn {
            background: red;
        }
        .header {
            font-size: 24px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h2>WhatsApp Auto Message Bot</h2>
    <p class="header">Welcome to the WhatsApp Auto Message Bot!</p>
    <form action="/" method="post">
        <button type="submit" name="action" value="start">Start Sending Messages</button>
        <button type="submit" name="action" value="stop" class="stop-btn">Stop Sending Messages</button>
    </form>
</body>
</html>
''')

if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Specify the port (5000) or any other available port
