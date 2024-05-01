from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import base64
from urllib.parse import urlparse


def take_screenshot(url, save_path):
    service = Service(executable_path='C:\\Program Files\\Webdriver\\chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Open the browser in full size
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(1)

    height = driver.execute_script("return document.body.scrollHeight")
    scroll_increment = 200
    current_scroll_position = 0
    while current_scroll_position < height:
        driver.execute_script(f"window.scrollTo(0, {current_scroll_position});")
        current_scroll_position += scroll_increment
        time.sleep(0.1)  # Small delay to allow page content to load
    # Scroll to the very bottom to ensure the footer is captured
    driver.execute_script(f"window.scrollTo(0, {height});")
    
    driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(0.5)


    # Use Chrome DevTools Protocol to capture the screenshot
    result = driver.execute_cdp_cmd("Page.captureScreenshot", {
        "format": "png",
        "captureBeyondViewport": True
    })
    screenshot = result['data']

    # Save the screenshot to a file
    with open(save_path, "wb") as file:
        file.write(base64.b64decode(screenshot))

    
    driver.quit()

def url_to_filename(url):
    path = urlparse(url).path
    filename = path.replace('/', '_')
    return filename


with open('urls.txt', 'r') as file:
    urls = file.read().splitlines()

for url in urls:
    take_screenshot(url, f"{url_to_filename(url)}.png")

