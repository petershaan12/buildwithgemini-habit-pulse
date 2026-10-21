import subprocess
import time
import os
import requests
import json

OUTPUT_DIR = "/config/.gemini/antigravity/brain/e2f16dd4-6c64-4c7e-b028-ba1521e5c17f"
FINAL_VIDEO_PATH = os.path.join(OUTPUT_DIR, "habit_pulse_demo.mp4")
FRONTEND_URL = "https://habit-pulse-frontend-1022414314284.us-east1.run.app"

# Start chrome in the X11 display
chrome_proc = subprocess.Popen([
    "google-chrome-stable",
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--window-size=1280,800",
    "--window-position=0,0",
    "--app=" + FRONTEND_URL
], env=dict(os.environ, DISPLAY=":1"))

time.sleep(3)

# Start ffmpeg recording screen :1
temp_video = "/tmp/screen_rec.mp4"
if os.path.exists(temp_video):
    os.remove(temp_video)

ffmpeg_proc = subprocess.Popen([
    "ffmpeg", "-y",
    "-f", "x11grab",
    "-video_size", "1280x800",
    "-i", ":1.0+0,0",
    "-c:v", "libx264",
    "-preset", "ultrafast",
    "-pix_fmt", "yuv420p",
    temp_video
])

print("Recording started...")
time.sleep(2)

# Use xdotool or python script to interact, or let's use playwright connected to CDP!
print("Done sleep")
