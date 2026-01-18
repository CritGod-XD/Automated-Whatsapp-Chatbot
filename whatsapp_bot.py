from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests


CHROMEDRIVER_PATH = "chromedriver.exe"
BOT_API_URL = "http://127.0.0.1:5000/chat_api"
USER_DATA_DIR = r"C:\Users\hp\Desktop\mohith_bot\chrome_profile_bot"



def clean_text(text):
    if not text:
        return ""
    return "".join(c for c in text if ord(c) <= 0xFFFF)


\
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={USER_DATA_DIR}")
options.add_argument("--profile-directory=Default")
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://web.whatsapp.com")
print("✅ WhatsApp opened. Waiting for login...")

WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.XPATH, "//div[@role='grid']"))
)

print("✅ Logged in. Bot is live 🤖")



last_seen_message = {}   




def get_chat_title():
    try:
        return driver.find_element(By.XPATH, "//header//span[@dir='auto']").text
    except:
        return None


def get_last_incoming_message():
    try:
        msgs = driver.find_elements(
            By.XPATH,
            "//div[contains(@class,'message-in')]//span[@dir='ltr']"
        )
        if msgs:
            return msgs[-1].text.strip()
    except:
        pass
    return None


def send_message(text):
    try:
        box = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@contenteditable='true'][@data-tab='10']")
            )
        )
        box.click()
        box.send_keys(clean_text(text))
        box.send_keys(Keys.ENTER)
    except Exception as e:
        print("⚠ Send failed:", e)


def call_bot_api(msg):
    try:
        r = requests.post(BOT_API_URL, json={"message": msg}, timeout=30)
        data = r.json()
        return data.get("reply", "").strip()
    except:
        return None


def check_current_chat():
    title = get_chat_title()
    if not title:
        return

    msg = get_last_incoming_message()
    if not msg:
        return

    if last_seen_message.get(title) == msg:
        return  

    print(f" ({title}) New message: {msg}")
    reply = call_bot_api(msg)

    if reply:
        print(f" Replying: {reply}")
        send_message(reply)

    last_seen_message[title] = msg


def handle_unread_chats():
    chats = driver.find_elements(
        By.XPATH,
        "//div[@role='row'][.//span[contains(@aria-label,'unread')]]"
    )

    for chat in chats:
       
        try:
            chat.find_element(By.XPATH, ".//span[@data-icon='default-group']")
            continue
        except:
            pass

        chat.click()
        time.sleep(2)
        check_current_chat()
        break


print(" Bot running (handles open + unread chats)\n")

while True:
    try:
        time.sleep(2)

        
        check_current_chat()

        
        handle_unread_chats()

    except KeyboardInterrupt:
        print("\n Bot stopped.")
        break

    except Exception as e:
        print(" Runtime error:", e)
        time.sleep(5)
