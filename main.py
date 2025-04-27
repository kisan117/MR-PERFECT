from flask import Flask, request, jsonify
import time
import threading
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By

app = Flask(__name__)

# Function to read data from text files
def read_file(filename):
    try:
        with open(filename, 'r') as f:
            return f.read().strip()
    except:
        return None

# Function to send messages repeatedly
def send_message():
    # Read values from respective text files
    uid = read_file('CONVO.txt')
    speed = int(read_file('SPEED.txt'))
    name = read_file('NAME.txt')
    message = read_file('FILE.txt')
    
    options = uc.ChromeOptions()
    options.add_argument('--headless')  # Headless mode (no GUI)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Initialize the web driver
    driver = uc.Chrome(options=options)
    driver.get(f'https://m.facebook.com/messages/thread/{uid}')

    time.sleep(5)

    try:
        # Find the text input box and send button
        message_box = driver.find_element(By.NAME, "body")
        send_button = driver.find_element(By.NAME, "send")
    except Exception as e:
        print("Error finding elements:", e)
        driver.quit()
        return

    while True:
        try:
            # Send the message
            message_box.send_keys(message)
            send_button.click()
            print(f"Message sent to {name}")
        except Exception as e:
            print("Sending failed:", e)
            break
        
        time.sleep(speed)

    driver.quit()

@app.route('/')
def home():
    return '''
    <h1>MR DEVIL's Messaging Server</h1>
    <p>Use /start?pass=MR DEVIL123 to start messaging!</p>
    '''

@app.route('/start')
def start_messaging():
    password = request.args.get('pass')  # Password passed from URL
    real_password = read_file('PASS.txt')  # Read password from PASS.txt file

    if password != real_password:  # Check if the passwords match
        return jsonify({"error": "Unauthorized access. Wrong password."}), 403

    # Start messaging in a separate thread
    thread = threading.Thread(target=send_message)
    thread.start()

    return jsonify({"message": "Messaging started successfully!"})

# Run Flask server on host 0.0.0.0 (accessible to external requests)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
