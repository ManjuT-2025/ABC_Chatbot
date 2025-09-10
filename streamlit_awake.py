from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Replace with your Streamlit app’s URL
APP_URL = "https://abc--chatbot.streamlit.app/"

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without visible browser window
chrome_options.add_argument("--no-sandbox")  # For GitHub Actions/Linux compatibility
chrome_options.add_argument("--disable-dev-shm-usage")  # Avoid memory issues
chrome_options.add_argument("--disable-gpu")  # Prevent GPU-related errors

# Initialize WebDriver with automatic ChromeDriver management
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # Visit the app URL
    driver.get(APP_URL)
    print(f"Visited {APP_URL}")

    # Wait for full page load (15 seconds for WebSocket connections)
    time.sleep(15)  # Adjust if your app loads slowly (e.g., 30 seconds for complex apps)

finally:
    # Close the browser
    driver.quit()
    print("Browser closed")