# import pywhatkit as pk
# import pyautogui
# import time
# import csv

# # Load contacts from CSV
# with open("contacts.csv", "r") as f:
#     reader = csv.DictReader(f)
#     contacts = [row for row in reader]

# # Your broadcast message
# message = "Hey! This is a test message for everyone. Double check if you received it."

# # Loop through each contact
# for idx, contact in enumerate(contacts):
#     number = contact["number"]
#     print(f"Sending to {contact['name']} ({number})...")

#     pk.sendwhatmsg_instantly(number, message, 15, True)  # 0 → don't auto-close
#     time.sleep(5)
#     pyautogui.press("enter")

#     # Small wait before moving to next person (avoid WhatsApp block)
#     if idx < len(contacts) - 1:
#         time.sleep(10)   # wait 10 sec before next send

# print("✅ Broadcast complete!")


import pywhatkit as pk
import pyautogui
import time
import csv


# Load contacts from CSV
with open("contacts.csv", "r") as f:
    reader = csv.DictReader(f)
    contacts = [row for row in reader]
    
for idx, contact in enumerate(contacts):
    number = contact["number"]
    name = contact["name"]
    due = contact["due_months"].strip()
    print(number,'-->', name,'-->', due)
    
    # Decide message
    if due == "":
        message = f"Hello {name},\nNo due. Just This month free ✅"
    else:
        message = f"Hello {name},\nYour child’s fee is due for: {due}"

    print(f"Sending to {name} ({number})...")

    pk.sendwhatmsg_instantly(number, message, 15, True)
    time.sleep(5)
    pyautogui.press("enter")
    
print("✅ Broadcast complete!")