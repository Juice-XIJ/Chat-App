import azure.cognitiveservices.speech as speechsdk
import constant
from logger import log
import time
import os


class tts():
    def __init__(self):
        self.synthesized = False
        with open(os.path.join('resources', 'tts.config', "ssml.xml"), "r") as ssml:
            self.ssml_string = ssml.read()

        speech_config = speechsdk.SpeechConfig(subscription=constant.api_key, region=constant.region)
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

        self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        def synthesis_cb(evt):
            try:
                result = evt.result
                if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                    first_byte_latency = int(evt.result.properties.get_property(speechsdk.PropertyId.SpeechServiceResponse_SynthesisFirstByteLatencyMs))
                    log.debug(constant.latency_log.format(self.speech_synthesis.__name__, first_byte_latency))
                elif result.reason == speechsdk.ResultReason.Canceled:
                    cancellation_details = result.cancellation_details
                    log.warning("Speech synthesis canceled: {}".format(cancellation_details.reason))
                    if cancellation_details.reason == speechsdk.CancellationReason.Error:
                        if cancellation_details.error_details:
                            log.exception("Error details: {}".format(cancellation_details.error_details))
                            log.exception("Did you set the speech resource key and region values?")
            except BaseException as e:
                log.exception(e)
            finally:
                self.synthesized = True

        self.speech_synthesizer.synthesis_completed.connect(synthesis_cb)
        self.speech_synthesizer.synthesis_canceled.connect(synthesis_cb)

        connection = speechsdk.Connection.from_speech_synthesizer(self.speech_synthesizer)
        connection.open(True)

    def speech_synthesis(self, txt):
        # The ssml string synthesize
        speech_synthesis_result = self.speech_synthesizer.start_speaking_ssml_async(self.generate_ssml(txt)).get()

        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioStarted:
            log.debug("Speech synthesizing for text [{}]".format(txt))

        while not self.synthesized:
            time.sleep(0.2)
            continue

        self.synthesized = False

    def generate_ssml(self, txt):
        constant.token_replace_mapping[constant.text_token] = txt
        ssml = self.ssml_string
        for token, value in constant.token_replace_mapping.items():
            ssml = ssml.replace(token, value)

        log.debug(ssml)
        return ssml
