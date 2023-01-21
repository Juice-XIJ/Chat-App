import constant
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


class key_word_detection():
    def __init__(self):
        self.byte_detected = False

        # ======== Hello Key Word =========
        # Creates an instance of a keyword recognition model.
        self.hello_model = speechsdk.KeywordRecognitionModel(constant.hello_key_word_model)

        # Create a local keyword recognizer with the default microphone device for input.
        self.hello_keyword_recognizer = speechsdk.KeywordRecognizer()

        def hello_recognized_cb(evt):
            # Only a keyword phrase is recognized. The result cannot be 'NoMatch'
            # and there is no timeout. The recognizer runs until a keyword phrase
            # is detected or recognition is canceled (by stop_recognition_async()
            # or due to the end of an input file or stream).
            result = evt.result
            if result.reason == speechsdk.ResultReason.RecognizedKeyword:
                log.debug("Hello KEYWORD: {}".format(result.text))

        def hello_canceled_cb(evt):
            result = evt.result
            if result.reason == speechsdk.ResultReason.Canceled and result.cancellation_details.reason != speechsdk.CancellationReason.EndOfStream:
                log.warning('CANCELED: {}'.format(result.cancellation_details.reason))

        # Connect callbacks to the events fired by the keyword recognizer.
        self.hello_keyword_recognizer.recognized.connect(hello_recognized_cb)
        self.hello_keyword_recognizer.canceled.connect(hello_canceled_cb)

        # ======= Bye Key Word =======
        # Creates an instance of a keyword recognition model.
        self.bye_model = speechsdk.KeywordRecognitionModel(constant.bye_key_word_model)

        # Create a local keyword recognizer with the default microphone device for input.
        self.bye_keyword_recognizer = speechsdk.KeywordRecognizer()

        def bye_recognized_cb(evt):
            # Only a keyword phrase is recognized. The result cannot be 'NoMatch'
            # and there is no timeout. The recognizer runs until a keyword phrase
            # is detected or recognition is canceled (by stop_recognition_async()
            # or due to the end of an input file or stream).
            self.result = evt.result
            if self.result.reason == speechsdk.ResultReason.RecognizedKeyword:
                self.byte_detected = True
                log.debug("Bye KEYWORD: {}".format(self.result.text))

        def bye_canceled_cb(evt):
            result = evt.result
            if result.reason == speechsdk.ResultReason.Canceled and result.cancellation_details.reason != speechsdk.CancellationReason.EndOfStream:
                log.warning('CANCELED: {}'.format(result.cancellation_details.reason))

        # Connect callbacks to the events fired by the keyword recognizer.
        self.bye_keyword_recognizer.recognized.connect(bye_recognized_cb)
        self.bye_keyword_recognizer.canceled.connect(bye_canceled_cb)

    def hello_keyword_locally_from_microphone(self):
        """runs keyword spotting locally, with direct access to the result audio"""
        # Start keyword recognition.
        result_future = self.hello_keyword_recognizer.recognize_once_async(self.hello_model)
        log.info('Say something starting with "{}" followed by whatever you want...'.format(constant.hello_keyword))
        result_future.get()

    def stop_hello_keyword_recognition(self):
        stop_future = self.hello_keyword_recognizer.stop_recognition_async()
        stop_future.get()
        log.debug('Stopped hello key word detection')

    def bye_keyword_locally_from_microphone(self):
        """runs keyword spotting locally, with direct access to the result audio"""
        # Start keyword recognition.
        result_future = self.bye_keyword_recognizer.recognize_once_async(self.bye_model)
        result_future.get()

    def stop_bye_keyword_recognition(self):
        stop_future = self.bye_keyword_recognizer.stop_recognition_async()
        stop_future.get()
        log.debug('Stopped bye key word detection')

    def is_bye_detected(self):
        return self.byte_detected

    def reset(self):
        self.stop_hello_keyword_recognition()
        self.stop_bye_keyword_recognition()
        self.byte_detected = False
