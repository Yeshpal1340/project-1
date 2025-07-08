from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.clock import Clock
from kivy.uix.label import Label
import threading
from pyzbar.pyzbar import decode
from PIL import Image
from gtts import gTTS
from plyer import audio
import os

class QRScannerLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.label = Label(text="Point camera at QR code", size_hint=(1, 0.1))
        self.add_widget(self.label)

        self.camera = Camera(play=True, resolution=(640, 480), size_hint=(1, 0.9))
        self.add_widget(self.camera)

        Clock.schedule_interval(self.scan_qr_code, 1)

    def scan_qr_code(self, dt):
        texture = self.camera.texture
        if not texture:
            return

        image_data = texture.pixels
        size = texture.size
        img = Image.frombytes(mode='RGBA', size=size, data=image_data)
        img = img.convert('L')  # grayscale

        qr_codes = decode(img)
        for code in qr_codes:
            qr_text = code.data.decode('utf-8')
            self.label.text = f"QR Code: {qr_text}"
            self.play_audio(qr_text)
            Clock.unschedule(self.scan_qr_code)

    def play_audio(self, text):
        def speak():
            tts = gTTS(text=text, lang='en')
            audio_file = "/sdcard/qr_audio.mp3"  # Android accessible path
            tts.save(audio_file)
            audio.play(path=audio_file)

        threading.Thread(target=speak, daemon=True).start()

class QRApp(App):
    def build(self):
        return QRScannerLayout()

if __name__ == '__main__':
    QRApp().run()
