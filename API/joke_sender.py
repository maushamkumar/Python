import smtplib
from email.mime.text import MIMEText

def send_email(joke, to_email):
    # Replace with your details
    sender_email = "maushamkumarr26@gmail.com"
    sender_password = "rqxz bfrr qdsa mrvq"  # Use app password if 2FA is on

    subject = "Here's a joke to brighten your day 😂"
    body = joke

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("✅ Email sent successfully!")
    except Exception as e:
        print("❌ Error sending email:", e)

# Example usage
if __name__ == "__main__":
    sample_joke = "Kya kar raha h ."
    recipient = input("Enter recipient email: ")
    send_email(sample_joke, recipient)
