from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pyautogui as pag
import time

# Initialize the WebDriver
service = Service('F:\Argha\WebDriver\chromedriver.exe')
driver = webdriver.Chrome(service=service)

def main():
    url = "http://linkedin.com/"
    driver.get(url)
    driver.maximize_window()

def login(username_input, password_input):
    try:
        username = driver.find_element(By.ID, "session_key")
        username.send_keys(username_input)
        
        password = driver.find_element(By.ID, "session_password")
        password.send_keys(password_input)
        
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(3)  # Allow time for the page to load
    except Exception as e:
        print(f"An error occurred during login: {e}")

def goto_network():
    try:
        driver.find_element(By.ID, "mynetwork-tab-icon").click()
        time.sleep(3)  # Allow time for the page to load
    except Exception as e:
        print(f"An error occurred while navigating to My Network: {e}")

def send_requests(n):
    try:
        for i in range(int(n)):
            pag.click(880, 770)  # Adjust position as necessary
            time.sleep(1)  # Add delay between requests
        print("Done!")
    except Exception as e:
        print(f"An error occurred while sending requests: {e}")

if __name__ == "__main__":
    main()
    login("your_username", "your_password")
    goto_network()
    num_requests = input("Number of requests: ")
    send_requests(num_requests)
    driver.quit()
