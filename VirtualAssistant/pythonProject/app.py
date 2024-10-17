import os
import speech_recognition as sr
import time

import datetime
import re
import webbrowser
import openai

import playsound
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from gtts import gTTS
from googletrans import Translator
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

language = 'vi'

path = ChromeDriverManager().install()


def speak(text):
    print("Mạnh: {}".format(text))
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("sound.mp3")
    playsound.playsound("sound.mp3", False)
    os.remove("sound.mp3")


def get_voice():
    print("Nhập câu hỏi của bạn: ", end='')
    text = input()
    if text:
        return text.lower()
    else:
        print("Không có đầu vào. Vui lòng thử lại.")
        return get_voice()


def stop():
    speak("Mình chào bạn nhé!")


def get_text():
    for i in range(3):
        text = get_voice()
        if text:
            return text.lower()
        elif i < 2:
            speak("Mình không nghe rõ, bạn có thể nói lại không ?")
    time.sleep(10)
    stop()
    return 0


def talk(name):
    day_time = int(strftime("%H"))
    if day_time < 12:
        speak("Chào buổi sáng {}. Chúc bạn ngày mới tốt lành!".format(name))
    elif day_time < 18:
        speak("Chào buổi chiều {}!".format(name))
    else:
        speak("Chào buổi tối {}!".format(name))


def open_web(text):
    rg = re.search(r'mở (.+)', text)
    if rg is not None:  # Ensure rg is not None before accessing group
        domain = rg.group(1)
        url = "https://www." + domain
        webbrowser.open(url)
        speak("Trang web của bạn đã được mở lên")
        return True
    else:
        speak("Xin lỗi, mình không hiểu yêu cầu mở trang web. Vui lòng thử lại.")
        return False


def get_time(text):
    now = datetime.datetime.now()
    if "giờ" in text:
        speak("Bây giờ là %d giờ %d phút" % (now.hour, now.minute))
    elif "ngày" in text:
        speak("Hôm nay là ngày %d tháng %d năm %d " % (now.day, now.month, now.year))
    else:
        speak("Mình không hiểu")

def google_search(text):
    search_for = text.split("kiếm", 1)[1].strip()

    if not search_for:
        speak("Xin lỗi, bạn chưa nhập nội dung cần tìm.")
        return

    speak("Đang tìm kiếm...")
    driver = webdriver.Chrome()

    try:
        # Open Google
        driver.get("https://www.google.com")
        query = driver.find_element(By.NAME, "q")
        query.send_keys(search_for)
        query.send_keys(Keys.RETURN)
    except Exception as e:
        speak("Có lỗi xảy ra khi tìm kiếm.")
        print(e)
    finally:
        time.sleep(5)
        driver.quit()

def main_func():
    speak("""Tôi có thể làm những việc sau:
     1. Chào hỏi
     2. Hiển thị giờ
     3. Mở website
     4. Tìm kiếm trên Google
     5. Gửi mail tự động 
     6. Dịch ngôn ngữ
      """)
    time.sleep(10)


def translate():
    speak("Bạn muốn dịch từ gì?")
    text_to_translate = input("Nhập từ bạn muốn dịch: ")

    if text_to_translate:
        speak("Bạn muốn dịch sang ngôn ngữ nào? Vui lòng nói tên ngôn ngữ.")
        target_language = str(input("Nhập ngôn ngữ bạn muốn dịch: "))

        languages = {
            "tiếng anh": "en",
            "tiếng việt": "vi",
            "tiếng pháp": "fr",
            "tiếng tây ban nha": "es",
            "tiếng đức": "de",
            "tiếng nhật": "ja",
            "tiếng hàn": "ko",
            "tiếng trung": "zh-CN",
        }

        target_language_code = languages.get(target_language.lower())
        if target_language_code:
            try:
                translator = Translator()
                translated = translator.translate(text_to_translate, dest=target_language_code)
                speak(f"Dịch từ '{text_to_translate}' sang '{target_language}': {translated.text}")
            except Exception as e:
                speak("Xin lỗi, có lỗi xảy ra trong quá trình dịch. Vui lòng thử lại.")
                print(f"Lỗi: {e}")
        else:
            speak("Xin lỗi, ngôn ngữ không hợp lệ. Vui lòng thử lại.")
    else:
        speak("Không có đầu vào để dịch. Vui lòng thử lại.")

def send_email():
    speak("Bạn muốn gửi email đến ai?")
    recipient_email = input("Nhập địa chỉ email người nhận: ")

    speak("Bạn muốn viết tiêu đề gì cho email?")
    subject = input("Nhập tiêu đề email: ")

    speak("Bạn muốn viết nội dung gì cho email?")
    body = input("Nhập nội dung email: ")
    sender_email = "your_email@gmail.com"
    sender_password = "your_password"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Nâng cấp kết nối
            server.login(sender_email, sender_password)
            server.send_message(msg)

        speak("Email đã được gửi thành công!")
    except Exception as e:
        speak("Có lỗi xảy ra khi gửi email.")
        print(e)
def call():
    speak("Xin chào! Bạn tên là gì nhì? ")
    time.sleep(1)
    name = get_text()
    if name:
        speak("Xin chào {}".format(name))
        time.sleep(3)
        speak("Bạn cần mình giúp gì !")
        time.sleep(2)
        while True:
            text = get_text()
            if not text:
                break
            elif "nói chuyện" in text or "trò chuyện" in text:
                talk(name)
            elif "dừng" in text or "thôi" in text:
                stop()
                break
            elif "mở" in text:
                if "mở google và tìm kiếm" in text:
                    google_search(text)
                else:
                    open_web(text)
            elif "ngày" in text or "giờ" in text:
                get_time(text)
            elif "có thể làm gì" in text:
                main_func()
            elif "dịch ngôn ngữ" in text:
                translate()
            elif "gửi mail" in text:
                send_email()


call()


