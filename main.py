import time

# Read target user ID from CONVO.txt
with open("CONVO.txt", "r") as file:
    target_id = file.read().strip()

# Read message speed (in seconds) from SPEED.txt
with open("SPEED.txt", "r") as file:
    speed = int(file.read().strip())

# Read message from FILE.txt
with open("FILE.txt", "r") as file:
    message = file.read().strip()

# Read Facebook token from TOKEN.txt
with open("TOKEN.txt", "r") as file:
    token = file.read().strip()

# Direct passcode hardcoded in the script
passcode = "MR_DEVIL123"  # Tumhara passcode jo tum hardcode karna chahte ho

# Function to send message
def send_message():
    print(f"Sending message to {target_id}: {message}")
    # Yeh jahan tum Facebook API ya automation code daloge message bhejne ke liye.

# Function to verify passcode before sending message
def verify_passcode():
    # Hardcoded passcode ko directly compare karenge
    entered_passcode = passcode  # Is case me passcode ko directly set kiya gaya hai
    if entered_passcode == passcode:
        print("Passcode correct. Sending message...")
        send_message()
    else:
        print("Incorrect passcode. Exiting.")
        exit()

# Verify passcode before proceeding
verify_passcode()

# Infinite loop to send messages repeatedly at specified speed
while True:
    send_message()
    time.sleep(speed)  # Wait for the specified speed time before sending the next message
