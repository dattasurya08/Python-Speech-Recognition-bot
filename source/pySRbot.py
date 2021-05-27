import speech_recognition as sr
import pyttsx3
import wolframalpha
import time

class TS_engine:
    def __init__(self):
        # TTS
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 160)
        self.tts_engine.setProperty('volume', 1.0)
        self.voices = self.tts_engine.getProperty('voices')
        self.tts_engine.setProperty('voice',self.voices[1].id)
        # STT
        self.stt_recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        # Wolframalpha
        self.client = wolframalpha.Client("4E44Q3-3WQT4J2U4V")

    def sayTTS(self, text, rec=False, recname='new_aud', format='wav'):
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
        if rec:
            recname = recname + '.' + format
            self.tts_engine.save_to_file(text, recname)
            self.tts_engine.runAndWait()

    def txtSTTaud(self, aud_file, sphinxEngine=False):
        try:
            src = self.stt_recognizer.AudioFile(aud_file)
            with src as source:
                self.stt_recognizer.adjust_for_ambient_noise(source)
                audio = self.stt_recognizer.record(source)
            if sphinxEngine:
                text = self.stt_recognizer.recognize_sphinx(audio)
            else:
                text = self.stt_recognizer.recognize_google(audio)
            return text
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("unknown error occured")

    def txtSTTmic(self, sphinxEngine=False):
        try:
            with self.mic as source:
                self.stt_recognizer.adjust_for_ambient_noise(source)
                audio = self.stt_recognizer.listen(source)
            if sphinxEngine:
                text = self.stt_recognizer.recognize_sphinx(audio)
            else:
                text = self.stt_recognizer.recognize_google(audio)
            return text
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("unknown error occured")
        return None


    def echoMicSpeech(self):
        mictext = self.txtSTTmic()
        echotxt = 'Did you say - ' + mictext + '?'
        self.sayTTS(echotxt)

    def QtoAwolframalpha(self):
        question = self.txtSTTmic()
        if question != None:
            print(question)
            try:
                res = self.client.query(question)
                ans = next(res.results).text
            except:
                ans = 'the question was not clear'
        else:
            ans = 'unknown error occured'
        print(ans)
        self.sayTTS(ans)


def main():
    ts = TS_engine()
    ts.sayTTS('Hi there. This is python voice assistant.')
    #ts.echoMicSpeech()
    while True:
        ts.sayTTS('Ask me a question')
        ts.QtoAwolframalpha()
        ts.sayTTS('would you like to ask again?')
        qa = ts.txtSTTmic()
        if (qa == 'no')|(qa == None):
            break


if __name__ == "__main__":
    main()
