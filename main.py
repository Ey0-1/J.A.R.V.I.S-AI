import os  # برای کار با فایل‌ها
import pyaudio  # برای ضبط صدا
import wave  # برای کار با فایل‌های WAV
import keyboard  # برای کنترل ورودی کیبورد
import time  # برای مدیریت زمان
import speech_recognition as sr  # برای تبدیل صدا به متن
import pyttsx3  # برای تبدیل متن به گفتار
from groq import Groq  # کتابخانه Groq AI

# تنظیمات Groq AI
client = Groq(api_key='###')  # کلید API خود را مستقیم وارد کنید
# ای پی ای کد باید خودتون از سایت گروک یا هر سایت ای ایی که میخواد بگیرید 

# تنظیمات ضبط صدا
FORMAT = pyaudio.paInt16  # فرمت صدای ضبط‌شده
CHANNELS = 1  # تعداد کانال‌ها (1 برای مونو)
RATE = 44100  # نرخ نمونه‌برداری
CHUNK = 1024  # اندازه بافر
OUTPUT_FILENAME = "recorded.wav"  # نام فایل WAV

# تابع برای ضبط صدا
def record_audio(duration=7):  # مدت زمان ضبط به ثانیه
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    frames = []
    print("Recording for {} seconds...".format(duration))
    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    # متوقف کردن جریان و بستن PyAudio
    stream.stop_stream()
    stream.close()  
    audio.terminate()

    # ذخیره فریم‌های ضبط‌شده به عنوان یک فایل WAV
    with wave.open(OUTPUT_FILENAME, 'wb') as wavefile:
        wavefile.setnchannels(CHANNELS)
        wavefile.setsampwidth(audio.get_sample_size(FORMAT))
        wavefile.setframerate(RATE)
        wavefile.writeframes(b''.join(frames))

# تابع برای تشخیص کلمه کلیدی
def listen_for_keyword(keywords):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)  # تنظیم برای نویز محیط
        print("Listening for keywords...")
        while True:
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio, language="en-US")  # تشخیص متن به زبان انگلیسی
                for keyword in keywords:
                    if keyword.lower() in text.lower():
                        print(f"Keyword '{keyword}' detected!")
                        return True
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                continue

# تابع اصلی
def main():
    keywords = ["heey", "lira heey", "heeeeeyy", "heylira", "heey lira", "heeey lira", "heeeeeey", "heey", "heeyn", "hey", "hhey", "heyy"]  # لیست کلمات کلیدی
    print("Voice assistant is running... Type 'exit' to quit.")
    
    while True:
        # از کاربر بخواهید که برای ادامه Enter را فشار دهد یا 'exit' را برای خروج وارد کند
        user_input = input("Press Enter to continue or type 'exit' to quit: ")
        if user_input.lower() == 'exit':
            print("Exiting the program...")
            break
        
        if listen_for_keyword(keywords):  # تشخیص کلمات کلیدی
            record_audio(7)  # شروع ضبط صدا به مدت 7 ثانیه
            process_audio()  # پردازش صوت و دریافت پاسخ

def process_audio():
    
    # تبدیل صدا به متن با استفاده از SpeechRecognition
    recognizer = sr.Recognizer()

    with sr.AudioFile(OUTPUT_FILENAME) as source:
        audio_data = recognizer.record(source)  # خواندن فایل صوتی
        try:
            print("Converting audio to text...")
            text = recognizer.recognize_google(audio_data, language="en-US")  # تبدیل صدا به متن
            print("Transcription:")
            print(text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
            return
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return

    # ارسال متن به Groq AI API
    if text:
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"{text}\nPlease respond with a concise and clear answer."  # درخواست پاسخ مختصر و مفید به زبان فارسی
                    }  
                ],
                model="llama-3.1-8b-instant"  # مدل مناسب برای تکمیل چت
            )

            answer = chat_completion.choices[0].message.content
            print("AI Response:")
            print(answer)

            # تبدیل پاسخ به صدا
            engine = pyttsx3.init()

            # یافتن صدای زنانه "Zira"
            voices = engine.getProperty('voices')
            for voice in voices:
                if "Zira" in voice.name:  # پیدا کردن صدای زنانه
                    engine.setProperty('voice', voice.id)
                    break
            else:
                print("Female voice Zira not found, using default voice.")

            engine.setProperty('rate', 180)  # تنظیم سرعت گفتار
            engine.setProperty('volume', 1)  # تنظیم حجم گفتار
            engine.say(answer)  # گفتن پاسخ
            engine.runAndWait()

        except Exception as e:
            print(f"Failed to get a response from Groq AI: {e}")

if __name__ == "__main__":
    main()



# تمامی کپشن ها توسط هوش مصنویی نوشته شده البته خودمم هم برسی کردم
# دوست دار شما NEECODE
