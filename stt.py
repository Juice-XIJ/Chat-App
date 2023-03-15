import constant
import time
from logger import log

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    log.error("""
    Importing the Speech SDK for Python failed.
    Refer to
    https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-python for
    installation instructions.
    """)
    import sys
    sys.exit(1)


class stt():
    def __init__(self):
        self.speech_config = speechsdk.SpeechConfig(subscription=constant.api_key, region=constant.region)
        self.speech_config.speech_recognition_language = constant.language

        self.audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=self.audio_config)

    def recognize_from_microphone(self, empty_count):
        start = time.time()
        log.debug("Speak into your microphone. {}".format(empty_count))

        # one short sentence
        speech_recognition_result = self.speech_recognizer.recognize_once_async().get()

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            log.info("You: {}".format(speech_recognition_result.text + '\n'))
        else:
            return ''

        # TODO: long sentence?
        # speech_recognition_result = speech_recognizer.start_continuous_recognition_async().get()

        end = time.time()
        log.debug(constant.latency_log.format(self.recognize_from_microphone.__name__, (end - start) * 1000))
        return speech_recognition_result.text
