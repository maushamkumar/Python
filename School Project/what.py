import pywhatkit as pk
import pyautogui
import time

# # Schedule message
pk.sendwhatmsg("+917548995419", "Kya kar raha h", 16, 38, 20, True, 2)

# # Wait for WhatsApp Web to load & type
# time.sleep(8)

# pk.sendwhatmsg_instantly("+917548995419", "Kya kar raha", 15, True, 2)

pyautogui.press("enter")   # Force send



# import pywhatkit as pk
# import pyautogui
# import time
# from datetime import datetime, timedelta

# def send_whatsapp_message(phone_no, message, hour=None, minute=None, delay_seconds=None):
#     """
#     phone_no: str (e.g., "+91700000419")
#     message: str
#     hour, minute: schedule time (24hr format)
#     delay_seconds: send after X seconds (alternative to exact time)
#     """

#     if delay_seconds:  
#         # Case 1: Send after a delay
#         time.sleep(delay_seconds)

#     elif hour is not None and minute is not None:  
#         # Case 2: Schedule at a specific time
#         now = datetime.now()
#         target_time = datetime(now.year, now.month, now.day, hour, minute)

#         # If target time already passed, schedule for next day
#         if target_time < now:
#             target_time += timedelta(days=1)

#         wait_time = (target_time - now).total_seconds()
#         print(f"Waiting {wait_time} seconds to send message...")
#         time.sleep(wait_time)

#     # Use instantly + manual enter (reliable on macOS)
#     pk.sendwhatmsg_instantly(phone_no, message, 15, True, 2)
#     time.sleep(5)
#     pyautogui.press("enter")
#     print("Message sent!")

# # # Example: send at 17:37
# # send_whatsapp_message("+917548995419", "Buss kaam kar jana", hour=18, minute=20)

# # # Example: send after 1 minute
# # # send_whatsapp_message("+91700000419", "Hello test", delay_seconds=60)


# import csv
# import json
# import random

# # Load contacts from CSV
# with open("contacts.csv", "r") as f:
#     reader = csv.DictReader(f)
#     contacts = [row for row in reader]

# # Load messages from JSON
# with open("messages.json", "r") as f:
#     messages = json.load(f)["messages"]

# # Test: Print contact + random message
# for contact in contacts:
#     name = contact["name"]
#     number = contact["number"]
#     message = random.choice(messages)  # Pick random message
    
#     send_whatsapp_message(number, message, hour=20, minute=14)
    
#     print(f"Sending to {name} ({number}): {message}")
