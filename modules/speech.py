import pyttsx3
import threading
import pythoncom

class Speaker:
    def __init__(self):
        self.last_spoken = ""
        self.lock = False

    def _speak_thread(self, text):
        try:
            pythoncom.CoInitialize()

            engine = pyttsx3.init(driverName='sapi5')
            engine.setProperty('rate', 165)
            engine.setProperty('volume', 1.0)

            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[0].id)

            engine.say(text)
            engine.runAndWait()
            engine.stop()

        except Exception as e:
            print("Speech Error:", e)

        self.lock = False

    def speak(self, text):
        if text and text != self.last_spoken and not self.lock:
            print("Speaking:", text)

            self.lock = True
            thread = threading.Thread(target=self._speak_thread, args=(text,))
            thread.daemon = True
            thread.start()

            self.last_spoken = text