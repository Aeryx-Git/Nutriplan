from playwright.sync_api import sync_playwright
import time

def scrape_instagram_post(url: str) -> str:
    """
    Uses Playwright to navigate to an Instagram post and extract the visible text,
    which usually includes the caption, comments, and any transcript text if available.
    """
    print(f"Starting Playwright to scrape: {url}")
    with sync_playwright() as p:
        # Launch browser in headless mode
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            # Go to the URL and wait until the network is idle
            page.goto(url, wait_until="networkidle")
            
            # Wait a few seconds for any dynamic content/captions to load
            time.sleep(3)
            
            # Extract the inner text of the body. 
            # The LLM will parse out the recipe from all the noise.
            text_content = page.evaluate("document.body.innerText")
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            text_content = ""
        finally:
            browser.close()
            
    return text_content
