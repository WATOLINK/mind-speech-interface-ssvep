import speech_recognition as sr

class SpeechToText():
    
    def __init__(self, index=0):
        '''Pass in index of the audio input you with to use, 0 is default input'''
        self.recog = sr.Recognizer()
        self.mic = sr.Microphone(device_index=index)

    def audioInputList():
        '''Lists all the audio inputs connected to the system'''
        print(sr.Microphone.list_microphone_names())

    def speechToText(self):
        '''Listens to audio from chosen input device and returns as string'''
        with self.mic as source:
            audio = self.recog.listen(source)
        try:
            text = self.recog.recognize_google(audio)
        except:
            return "Err"
        return text
        