import subprocess
from pathlib import Path
import os
import time

def clear_folder():
    # Clears the frames folder for the current video
    folder = Path("frames")     # You must make a 'frames' folder manually
    for file in folder.glob("*"):
        file.unlink()
    return

def create_frames(video_path):
    os.makedirs("frames", exist_ok=True)

    # takes 1 frame per second and puts it into the frames folder
    subprocess.run([
        r"/opt/homebrew/bin/ffmpeg",
        "-hwaccel", "auto",
        "-i", video_path,
        "-vf", "fps=1",
        "-q:v", "31",      # this value changes the frame quality
        "frames/%04d.jpg"
    ])

