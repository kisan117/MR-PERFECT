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

# Read passcode from PASS.txt
with open("PASS.txt", "r") as file:
    passcode = file.read().strip()

# Function to send message
def send_message():
    print(f"Sending message to {target_id}: {message}")
    # Here you would integrate your messaging code using the token.
    # This could be a direct API request, for example.

# Function to verify passcode
def verify_passcode():
    entered_passcode = input("Enter passcode: ")
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
