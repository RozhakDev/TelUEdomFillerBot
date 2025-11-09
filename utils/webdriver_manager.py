from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_driver():
    """Initializes and returns a Chrome WebDriver instance.

    This function configures the Chrome browser to:
    - Start in maximized mode.
    - Open with a custom offset position (centered on screen with defined dimensions).

    The browser window is positioned manually by calculating the offset from
    screen resolution (assumed 1920x1080) and the browser window size (900x700).

    Returns:
        selenium.webdriver.Chrome: Configured Chrome WebDriver instance.
    """
    options = Options()
    options.add_argument('--start-maximized')

    x = (1920 - 900) // 2  # Horizontal offset from left
    y = (1080 - 700) // 2  # Vertical offset from top
    options.add_argument(f"--window-position={x},{y}")

    driver = webdriver.Chrome(options=options)
    return driver