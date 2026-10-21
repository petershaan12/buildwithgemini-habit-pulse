import asyncio
import os
import shutil
import subprocess
import time
from playwright.async_api import async_playwright

FRONTEND_URL = "https://habit-pulse-frontend-1022414314284.us-east1.run.app"
OUTPUT_DIR = "/config/.gemini/antigravity/brain/e2f16dd4-6c64-4c7e-b028-ba1521e5c17f"
RAW_VIDEO_DIR = "/tmp/playwright_videos"
FINAL_VIDEO_NAME = "habit_pulse_demo.mp4"
FINAL_VIDEO_PATH = os.path.join(OUTPUT_DIR, FINAL_VIDEO_NAME)

os.makedirs(RAW_VIDEO_DIR, exist_ok=True)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path="/usr/bin/google-chrome-stable",
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--window-size=1280,800"
            ]
        )
        context = await browser.new_context(
            record_video_dir=RAW_VIDEO_DIR,
            record_video_size={"width": 1280, "height": 800},
            viewport={"width": 1280, "height": 800}
        )
        page = await context.new_page()

        print("Navigating to frontend...")
        await page.goto(FRONTEND_URL, wait_until="networkidle")
        await asyncio.sleep(2)

        # 1. Prompt 1: Show active habits & user status (core functionality)
        print("Sending Prompt 1...")
        prompt1 = "Show my active habits and current streak status"
        await page.fill("#input", prompt1)
        await asyncio.sleep(1)
        await page.click("button.send-btn")

        # Wait for agent response
        print("Waiting for response 1...")
        for _ in range(30):
            agent_msgs = await page.locator(".msg.agent").all()
            if len(agent_msgs) > 1:
                last_text = await agent_msgs[-1].inner_text()
                if "…" not in last_text and "Error" not in last_text:
                    print("Received response 1!")
                    break
            await asyncio.sleep(1)

        await asyncio.sleep(3)

        # 2. Prompt 2: Rich prompt with tool call / logging / badge generation
        print("Sending Prompt 2...")
        prompt2 = "I just drank a glass of water! Log my habit completion, award XP, and generate an achievement image for Sprout"
        await page.fill("#input", prompt2)
        await asyncio.sleep(1)
        await page.click("button.send-btn")

        print("Waiting for response 2...")
        for _ in range(60):
            agent_msgs = await page.locator(".msg.agent").all()
            if len(agent_msgs) > 2:
                last_text = await agent_msgs[-1].inner_text()
                if "…" not in last_text:
                    print("Received response 2!")
                    break
            await asyncio.sleep(2)

        await asyncio.sleep(4)

        # Scroll to bottom smoothly to showcase cards
        await page.evaluate("document.getElementById('log').scrollTop = document.getElementById('log').scrollHeight")
        await asyncio.sleep(3)

        await context.close()
        await browser.close()

    # Find the recorded webm/mp4 video from playwright
    video_files = [f for f in os.listdir(RAW_VIDEO_DIR) if f.endswith((".webm", ".mp4"))]
    if not video_files:
        print("No video recorded by Playwright.")
        return

    latest_video = max([os.path.join(RAW_VIDEO_DIR, f) for f in video_files], key=os.path.getmtime)
    print(f"Recorded video: {latest_video}")

    # Convert to standard MP4 using ffmpeg for artifact viewer
    print(f"Converting to {FINAL_VIDEO_PATH}...")
    cmd = [
        "ffmpeg", "-y", "-i", latest_video,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        FINAL_VIDEO_PATH
    ]
    subprocess.run(cmd, check=True)
    print("Done! Demo video saved to:", FINAL_VIDEO_PATH)

if __name__ == "__main__":
    asyncio.run(main())
