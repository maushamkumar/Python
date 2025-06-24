import streamlit as st  
import requests
import random
from streamlit_autorefresh import st_autorefresh
from email.mime.text import MIMEText

# Optional: Refresh every 30 seconds
# st_autorefresh(interval=30 * 1000, key="refresh")

st.set_page_config(page_title="Joke Fetcher", page_icon="😂")

# st.title("😂 Random Joke Generator")
st.title("😂 Random Joke Generator + Emailer")

# category = st.selectbox("Choose category", ["Any", "Programming", "Misc", "Dark", "Pun"])
# joke_url = f"https://v2.jokeapi.dev/joke/{category}?type=single" if category != "Any" else "https://v2.jokeapi.dev/joke/Any"


def send_email(joke, recipient_email):
    sender_email = "maushamkumarr26@gmail.com"
    sender_password = "rqxz bfrr qdsa mrvq"
    
    subject = "Here's your daily joke! 😂"
    body = joke
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email
    
    try: 
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        st.success("✅ Email sent successfully!")
    except Exception as e:
        st.error(f"❌ Error sending email: {e}")
        return False
    
    
# Sidebar for options
st.sidebar.title("Options")
    
    

with st.sidebar:
    st.header("🎯 Joke Options")
    category = st.selectbox("Choose category", ["Any", "Programming", "Misc", "Dark", "Pun"])
    blacklist = []
    if st.checkbox("Filter NSFW"):
        blacklist.append("nsfw")
    if st.checkbox("Filter Religious"):
        blacklist.append("religious")
    if st.checkbox("Filter Political"):
        blacklist.append("political")

flags = ",".join(blacklist)
joke_url = f"https://v2.jokeapi.dev/joke/{category}?blacklistFlags={flags}"

# Background styling using CSS
# st.markdown("""
#     <style>
#     .stApp {
#         background-image: url('https://media.giphy.com/media/f9k1tV7HyORcngKF8v/giphy.gif');
#         background-size: cover;
#     }
#     </style>
# """, unsafe_allow_html=True)


# Refresh every 30 sec
st_autorefresh(interval=30 * 1000, key="refresh")

# Handle button clicks using session state
if "joke" not in st.session_state:
    st.session_state.joke = ""

# joke_url = f"https://v2.jokeapi.dev/joke/{category}?blacklistFlags=nsfw,religious,political"
emojis = ["😂", "🤣", "😜", "🙃", "😆", "🤪", "🎭", "🧠", "👻"]
reaction = random.choice(emojis)
st.markdown(f"## {reaction} Here's your joke!")
if st.button("Get a Joke"):
    response = requests.get(joke_url)
    if response.status_code == 200:
        data = response.json()
        # if data["type"] == "single":
        #     joke = data["joke"]
        #     st.subheader("Joke:")
        #     st.write(data["joke"])
        # elif data["type"] == "twopart":
        #     st.subheader("Setup:")
        #     st.write(data["setup"])
        #     st.subheader("Punchline:")
        #     st.write(data["delivery"])
        if data["type"] == "single":
            joke = data["joke"]
        else:
            joke = f"{data['setup']} — {data['delivery']}"

        st.session_state.joke = joke  # ✅ STORE THE JOKE
        st.code(joke)

        
        
        # if st.button("❤️ Save Joke"):
        #     with open("my_jokes.txt", "a") as f:
        #         f.write(joke + "\n---\n")
        #     st.success("Joke saved!")


        
    else:
        st.error("Failed to fetch joke. Try again later.")
        
# Display the joke if exists
if st.session_state.joke:
    st.code(st.session_state.joke)

    # Copy mock button
    st.button("📋 Copy this joke", on_click=lambda: st.write("✅ Copied! (Just imagine 😅)"))

    # Save joke to file
    if st.button("❤️ Save Joke"):
        with open("my_jokes.txt", "a", encoding="utf-8") as f:
            f.write(st.session_state.joke + "\n---\n")
        st.success("Joke saved!")