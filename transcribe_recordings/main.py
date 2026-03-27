import asyncio
from playwright.async_api import async_playwright

URL="" # env file

async def get_zoom_video():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Disable headless
        page = await browser.new_page()
        
        video_url = None
        
        async def handle_response(response):
            nonlocal video_url
            if '.mp4' in response.url:
                video_url = response.url
                print(f"✅ Found video URL: {video_url}")
        
        page.on("response", handle_response)
        await page.goto(URL)
        await page.wait_for_timeout(3000)
        
        # Click the play button
        try:
            play_button = await page.query_selector('button[aria-label="Play"]')
            if play_button:
                await play_button.click()
                print("▶️ Clicked play button")
            else:
                # Try alternative selectors
                await page.click('[class*="play"]')
                print("▶️ Clicked play")
        except Exception as e:
            print(f"⚠️ Could not click play: {e}")
        
        # Wait 10 seconds for video to start
        await page.wait_for_timeout(10000)

        # Download WHILE browser is still open
        if video_url:
            print("📥 Downloading video...")
            response = await page.request.get(video_url)
            if response.status == 200:
                with open("recording.mp4", "wb") as f:
                    f.write(await response.body())
                print("✅ Video downloaded successfully!")
            else:
                print(f"❌ Failed: {response.status}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(get_zoom_video())