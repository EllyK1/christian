import os, json, random, webbrowser, sounddevice as sd, smtplib
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.listview import ListView, ListItemButton
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window
from scipy.io.wavfile import write
from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF
import pyrebase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Firebase Config
firebaseConfig = {
  "apiKey": "AIzaSyCctpf2MmcNJaDTu4x1Te8muDIm2BuKYdo",
  "authDomain": "christianapp-2b6e4.firebaseapp.com",
  "projectId": "christianapp-2b6e4",
  "storageBucket": "christianapp-2b6e4.firebasestorage.app",
  "messagingSenderId": "880005280370",
  "appId": "1:880005280370:web:db6b425ffff9b9099f48eb",
  "measurementId": "G-4WZ8WZWK1J",
  "databaseURL": "https://christianapp-2b6e4-default-rtdb.firebaseio.com/"
}
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

# Email Config
EMAIL_SENDER = "emailbridge453@gmail.com"
EMAIL_PASSWORD = "your_app_password_here"
EMAIL_RECEIVER = "emailbridge453@gmail.com"

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
    except Exception as e:
        print("Email error:", e)

# Load Bible JSON files
def load_bible(folder):
    bible = {}
    for file in os.listdir(folder):
        if file.endswith(".json"):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "book" in data and "chapters" in data:
                    bible[data["book"]] = data
    return bible

bible = load_bible("D:\\quiz_generator\\Christian_app\\Bible-kjv-master")

def search_bible(keyword, bible):
    results = []
    keyword = keyword.lower()
    for book, book_data in bible.items():
        for chapter in book_data["chapters"]:
            for verse in chapter["verses"]:
                if keyword in verse["text"].lower():
                    results.append(f'{book} {chapter["chapter"]}:{verse["verse"]} - {verse["text"]}')
    return results

def get_encouragement(user_text, bible):
    verses_found = search_bible(user_text, bible)
    if verses_found:
        return random.choice(verses_found)
    else:
        return "Psalm 23:1 - The Lord is my shepherd; I shall not want."

class ChristianApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Language Selector
        self.lang_selector = Spinner(text="en", values=["en","fr","de","it","nl","sv"])
        self.add_widget(Label(text="🌍 Select Language"))
        self.add_widget(self.lang_selector)

        # Daily Verse
        self.verse_label = Label(text="📖 Daily Verse will appear here")
        self.add_widget(self.verse_label)
        verse_btn = Button(text="Show Daily Verse")
        verse_btn.bind(on_press=self.show_daily_verse)
        self.add_widget(verse_btn)

        # Scripture Request
        self.email_input = TextInput(hint_text="Enter your email")
        self.add_widget(self.email_input)
        self.request_input = TextInput(hint_text="Type your scripture request here...", multiline=True)
        self.add_widget(self.request_input)
        request_btn = Button(text="Request Scripture")
        request_btn.bind(on_press=self.save_request)
        self.add_widget(request_btn)

        # Puzzle Request
        self.puzzle_input = TextInput(hint_text="Type your puzzle/quiz request here...", multiline=True)
        self.add_widget(self.puzzle_input)
        puzzle_btn = Button(text="Request Puzzle/Quick Question")
        puzzle_btn.bind(on_press=self.save_puzzle)
        self.add_widget(puzzle_btn)

        # Encouragement
        self.problem_input = TextInput(hint_text="Type your problem here...", multiline=True)
        self.add_widget(self.problem_input)
        encourage_btn = Button(text="Get Encouragement Verse")
        encourage_btn.bind(on_press=self.show_encouragement)
        self.add_widget(encourage_btn)

        # Prayer Wall
        self.prayer_input = TextInput(hint_text="Type your prayer request here...", multiline=True)
        self.add_widget(self.prayer_input)
        prayer_btn = Button(text="Post Prayer Request")
        prayer_btn.bind(on_press=self.save_prayer)
        self.add_widget(prayer_btn)

        # Testimony Recording
        record_btn = Button(text="Record Testimony")
        record_btn.bind(on_press=self.record_testimony)
        self.add_widget(record_btn)

        # Meme Creator
        meme_btn = Button(text="Create Meme (PNG + PDF)")
        meme_btn.bind(on_press=self.create_meme)
        self.add_widget(meme_btn)

        # Sharing
        self.add_widget(Label(text="📢 Share"))
        fb_btn = Button(text="Share on Facebook")
        fb_btn.bind(on_press=lambda x: webbrowser.open("https://www.facebook.com/sharer/sharer.php?u=https://christianapp"))
        self.add_widget(fb_btn)

        wa_btn = Button(text="Share on WhatsApp")
        wa_btn.bind(on_press=lambda x: webbrowser.open("https://api.whatsapp.com/send?text=Blessings%20from%20Christian%20App"))
        self.add_widget(wa_btn)

        insta_btn = Button(text="Share on Instagram")
        insta_btn.bind(on_press=lambda x: webbrowser.open("https://www.instagram.com"))
        self.add_widget(insta_btn)

        tw_btn = Button(text="Share on Twitter")
        tw_btn.bind(on_press=lambda x: webbrowser.open("https://twitter.com/intent/tweet?text=Blessings%20from%20Christian%20App"))
        self.add_widget(tw_btn)

        # Support
        donate_btn = Button(text="Donate via PayPal")
        donate_btn.bind(on_press=lambda x: webbrowser.open("https://www.paypal.com/ncp/payment/QXN7AHRFCGM3L"))
        self.add_widget(donate_btn)

    def show_daily_verse(self, instance):
        book = random.choice(list(bible.keys()))
        book_data = bible[book]
        chapter = random.choice(book_data["chapters"])
        verse = random.choice(chapter["verses"])
        self.verse_label.text = f'{book} {chapter["chapter"]}:{verse["verse"]} - {verse["text"]}'

    def show_encouragement(self, instance):
        keyword = self.problem_input.text.strip()
        verse = get_encouragement(keyword, bible)
        self.verse_label.text = f"Encouragement: {verse}"
        db.child("problems").push({"email": self.email_input.text(), "problem": keyword})
        send_email("New Problem Request", f"User problem: {keyword}\nSuggested verse: {verse}")

    def save_request(self, instance):
        email = self.email_input.text
        request_text = self.request_input.text
        lang = self.lang_selector.text
        if email and request_text:
            db.child("requests").push({"email": email, "request": request_text, "lang": lang})
            send_email("New Scripture Request", f"User scripture request: {request_text} (lang: {lang})")

    def save_puzzle(self, instance):
        email = self.email_input.text
        puzzle_text = self.puzzle_input.text
        lang = self.lang_selector.text
        if email and puzzle_text:
            db.child("puzzles").push({"email": email, "puzzle": puzzle_text, "lang": lang})
            send_email("New Puzzle Request", f"User puzzle request: {puzzle_text} (lang: {lang})")

       def save_prayer(self, instance):
        email = self.email_input.text
        prayer_text = self.prayer_input.text
        lang = self.lang_selector.text
        if email and prayer_text:
            db.child("prayers").push({"email": email, "prayer": prayer_text, "lang": lang})
            send_email("New Prayer Request", f"User prayer request: {prayer_text} (lang: {lang})")
            self.verse_label.text = "Prayer posted successfully."
        else:
            self.verse_label.text = "Error: Please enter your email and prayer request."

    def record_testimony(self, instance):
        fs = 44100
        duration = 30  # default 30 seconds, can be adjusted
        self.verse_label.text = f"Recording testimony for {duration} seconds..."
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        filename = "testimony.wav"
        write(filename, fs, recording)
        self.verse_label.text = f"Recording saved as {filename}"

    def create_meme(self, instance):
        text = self.request_input.text.strip()
        if not text:
            self.verse_label.text = "Error: Please type scripture or encouragement text."
            return
        img = Image.new('RGB', (600, 400), color=(73, 109, 137))
        d = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        d.text((10, 180), text, fill=(255, 255, 255), font=font)

        # Save PNG
        filename = "meme.png"
        img.save(filename)
        self.verse_label.text = f"Meme saved as {filename}"

        # Also save PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.image(filename, x=10, y=10, w=180)
        pdf_filename = "meme.pdf"
        pdf.output(pdf_filename)
        self.verse_label.text = f"Meme PDF saved as {pdf_filename}"

class ChristianAppMain(App):
    def build(self):
        return ChristianApp()

if __name__ == "__main__":
    ChristianAppMain().run()
