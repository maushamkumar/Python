from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os 
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

speech_file_path = Path("speech2.mp3")

text = """
आज का दिन कुछ अलग सा है…
जैसे मन खुद से कह रहा हो —
चलो, कुछ ऐसा बनाते हैं
जिसे लोग सच में याद रखें।
"""

with client.audio.speech.with_streaming_response.create(
    model="tts-1-hd",
    voice="shimmer",
    input=text,
    response_format="mp3"
) as response:
    response.stream_to_file(speech_file_path)

print("Saved:", speech_file_path.resolve())
