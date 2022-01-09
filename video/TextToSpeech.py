from gtts import gTTS
from mutagen.mp3 import MP3
import os

class TextToSpeech:
    def __init__(self, language: str = 'en', tld: str = 'ca') -> None:
        self.language = language
        self.tld = tld

    def get_duration(self, text: str, slow: bool = False) -> float:
        savefile = 'tmp.mp3'
        mp3 = gTTS(text=text, lang=self.language, slow=slow, tld=self.tld)
        mp3.save(savefile)
        duration = MP3(savefile).info.length
        os.remove(savefile)
        return duration

    def save(self, text: str, savefile: str, slow: bool = False) -> None:
        mp3 = gTTS(text=text, lang=self.language, slow=slow, tld=self.tld)
        mp3.save(savefile)