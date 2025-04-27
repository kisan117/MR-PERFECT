import os
import time
import requests
import signal
import sys

# Yeh server MR DEVIL ne create kiya hai
# Author: ME DEVIL
# File Paths
TOKEN_FILE = 'TOKEN.txt'
NAME_FILE = 'NAME.txt'
FILE_FILE = 'FILE.txt'
SPEED_FILE = 'SPEED.txt'
CONVO_FILE = 'CONVO.txt'
PASS_FILE = 'PASS.txt'  # Password file for additional security
LOG_FILE = 'server_log.txt'  # Log file for actions

# Function to read local files
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

# Function to write logs to a file
def write_log(message):
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(message + "\n")

# Function to check password
def check_password():
    correct_password = "MR DEVIL SERVER CREATER"  # Hardcoded password
    entered_password = input("Enter the password to start the server: ").strip()
    
    if entered_password == correct_password:
        write_log("Password is correct. Starting the message sender...")
        return True
    else:
        write_log("Incorrect password attempt. Exiting...")
        print("Incorrect password. Exiting...")
        sys.exit(1)

# Fetch data from files
def load_config():
    try:
        token = read_file(TOKEN_FILE)  # Read from local files
        name = read_file(NAME_FILE)
        file_content = read_file(FILE_FILE)
        speed = read_file(SPEED_FILE)
        convo_id = read_file(CONVO_FILE)
        return token, name, file_content, speed, convo_id
    except FileNotFoundError:
        write_log("Error: One or more files are missing.")
        return None, None, None, None, None

# Function to send message via Facebook Graph API
def send_message(convo_id, message, token, speed):
    # Facebook Graph API URL to send message
    url = f"https://graph.facebook.com/v14.0/{convo_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
    }
    payload = {
        "message": {
            "text": message  # Just send the actual message
        }
    }
    
    # Sending POST request to Facebook API
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        log_message = f"Message sent by MR DEVIL: {message}"
        print(log_message)
        write_log(log_message)
    else:
        log_message = f"Error sending message (Status Code: {response.status_code}): {response.text}"
        print(log_message)
        write_log(log_message)
    
    # Simulate delay based on SPEED.txt (milliseconds)
    time.sleep(int(speed) / 1000)  # Convert speed to seconds

# Graceful Shutdown
def handle_shutdown_signal(signal, frame):
    log_message = "\nGracefully shutting down the message sender..."
    print(log_message)
    write_log(log_message)
    sys.exit(0)

# Main function to start the message sending process
def start_message_sending():
    # Check password before starting the server
    if not check_password():
        return
    
    token, name, file_content, speed, convo_id = load_config()
    
    if not all([token, name, file_content, speed, convo_id]):
        log_message = "Error: One or more files are missing."
        print(log_message)
        write_log(log_message)
        return

    # Construct message
    message = f"Hello {name}, this is a test message! Content: {file_content}"
    
    # Setup graceful shutdown on signal (Ctrl+C or SIGINT)
    signal.signal(signal.SIGINT, handle_shutdown_signal)

    log_message = "Message sending started... Press Ctrl+C to stop."
    print(log_message)
    write_log(log_message)
    
    # Start sending messages repeatedly until manually stopped
    while True:
        # Print log message with sender's name before sending
        log_message = f"Message sent by MR DEVIL: {message}"
        print(log_message)
        write_log(log_message)
        
        send_message(convo_id, message, token, speed)

# Run the function
if __name__ == '__main__':
    # Port setup for Render environment (binding to port 10000)
    port = int(os.environ.get("PORT", 10000))  # Use the PORT environment variable
    start_message_sending()
