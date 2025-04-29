import pywhatkit as kit
import time

def send_message():
    # User se input lena
    my_number = input("Apna number likho (+91XXXXXXXXXX): ")
    target_number = input("Target number likho (+91XXXXXXXXXX): ")
    group_name = input("Group name likho (agar hai toh): ")
    message = input("Message jo bhejna hai likho: ")
    speed = int(input("Speed set karo (seconds per message): "))

    print("Message bhejna shuru kar rahe hain...")

    # WhatsApp Web pe message bhejna pywhatkit se
    kit.sendwhatmsg(target_number, message, 14, 0)  # Set the time, yaha time set hoga
    time.sleep(speed)  # Speed set karenge ki kitni der baad message bhejna hai

    print(f"Message sent to {target_number} successfully!")

# Script ko run karte waqt call karenge
send_message()
