import os
import subprocess

def wav_to_mp3(
    input_wav_path: str,
    output_mp3_path: str,
    bitrate: str = "192k"
):
    """
    Converts a WAV audio file to MP3 using ffmpeg.

    Args:
        input_wav_path (str): Path to input .wav file
        output_mp3_path (str): Path to output .mp3 file
        bitrate (str): MP3 bitrate (e.g. 128k, 192k, 320k)
    """

    if not os.path.exists(input_wav_path):
        raise FileNotFoundError("Input WAV file not found")

    command = [
        "ffmpeg",
        "-y",                 # overwrite output if exists
        "-i", input_wav_path,
        "-vn",                # no video
        "-acodec", "libmp3lame",
        "-ab", bitrate,
        output_mp3_path
    ]

    subprocess.run(command, check=True)
    print(f"Converted WAV → MP3: {output_mp3_path}")


# Example usage
wav_to_mp3(
    input_wav_path="download (2).wav",
    output_mp3_path="output.mp3",
    bitrate="192k"
)
