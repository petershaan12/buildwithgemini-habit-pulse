import asyncio
import os
import subprocess
import time
from playwright.async_api import async_playwright

OUTPUT_DIR = "/config/.gemini/antigravity/brain/e2f16dd4-6c64-4c7e-b028-ba1521e5c17f"
FINAL_VIDEO_PATH = os.path.join(OUTPUT_DIR, "habit_pulse_demo.mp4")
FRONTEND_URL = "https://habit-pulse-frontend-1022414314284.us-east1.run.app"
temp_video = "/tmp/screen_rec.mp4"

# 1. Start Chrome with remote debugging on :1
chrome_proc = subprocess.Popen([
    "google-chrome-stable",
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--remote-debugging-port=9222",
    "--window-size=1280,800",
    "--window-position=0,0",
    "--user-data-dir=/tmp/chrome_demo_profile",
    FRONTEND_URL
], env=dict(os.environ, DISPLAY=":1"))

time.sleep(3)

# 2. Start ffmpeg recording screen :1
if os.path.exists(temp_video):
    os.remove(temp_video)

ffmpeg_proc = subprocess.Popen([
    "ffmpeg", "-y",
    "-f", "x11grab",
    "-video_size", "1280x800",
    "-framerate", "25",
    "-i", ":1.0+0,0",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-preset", "ultrafast",
    temp_video
])

print("Screen recorder started...")

async def run_actions():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else await context.new_page()

        print("Waiting for page load...")
        await page.wait_for_selector("#input", timeout=15000)
        await asyncio.sleep(2)

        # Action 1: Click the quick prompt chip "📋 View Today's Habits"
        print("Clicking prompt chip 1...")
        chips = await page.locator(".chip").all()
        if chips:
            await chips[0].click()
        else:
            await page.fill("#input", "Show my active habits and current streak status")
            await page.click("button.send-btn")

        print("Waiting for Agent response to prompt 1...")
        # Wait until response arrives
        for _ in range(40):
            agent_msgs = await page.locator(".msg.agent").all()
            if len(agent_msgs) > 1:
                last_text = await agent_msgs[-1].inner_text()
                if "…" not in last_text:
                    print("Prompt 1 response rendered!")
                    break
            await asyncio.sleep(1)

        await asyncio.sleep(3)

        # Action 2: Rich prompt with habit completion, Firestore update, XP, and mascot image generation
        print("Typing rich Prompt 2...")
        prompt2 = "I just drank a glass of water! Log my habit completion, award XP, and generate an achievement image for Sprout"
        await page.fill("#input", prompt2)
        await asyncio.sleep(1)
        await page.click("button.send-btn")

        print("Waiting for Agent response to prompt 2 (including image tool call)...")
        for _ in range(60):
            agent_msgs = await page.locator(".msg.agent").all()
            if len(agent_msgs) > 2:
                last_text = await agent_msgs[-1].inner_text()
                if "…" not in last_text:
                    print("Prompt 2 response rendered with rich A2UI card & image!")
                    break
            await asyncio.sleep(1)

        await asyncio.sleep(4)

        # Scroll to bottom
        await page.evaluate("document.getElementById('log').scrollTop = document.getElementById('log').scrollHeight")
        await asyncio.sleep(3)

asyncio.run(run_actions())

# Stop ffmpeg and chrome
print("Stopping recording...")
ffmpeg_proc.terminate()
try:
    ffmpeg_proc.wait(timeout=5)
except Exception:
    ffmpeg_proc.kill()

chrome_proc.terminate()
try:
    chrome_proc.wait(timeout=5)
except Exception:
    chrome_proc.kill()

# Copy to final destination
if os.path.exists(temp_video):
    cmd = [
        "ffmpeg", "-y", "-i", temp_video,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        FINAL_VIDEO_PATH
    ]
    subprocess.run(cmd, check=True)
    print("SUCCESS: Demo video saved to", FINAL_VIDEO_PATH)
else:
    print("ERROR: Recording failed to produce temp video")
