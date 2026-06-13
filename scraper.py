from playwright.sync_api import sync_playwright

def test_environment():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.hasznaltauto.hu")
        print("Environment has been set and the page loaded succesfully!")
        browser.close()

if __name__ == "__main__":
    test_environment()