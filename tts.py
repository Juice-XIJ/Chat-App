import azure.cognitiveservices.speech as speechsdk
import constant
from logger import log
import os


class tts():
    def __init__(self):
        self.synthesized = False
        with open(os.path.join('resources', 'tts.config', "ssml.xml"), "r") as ssml:
            self.ssml_string = ssml.read()

        speech_config = speechsdk.SpeechConfig(subscription=constant.api_key, region=constant.region)
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

        self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        connection = speechsdk.Connection.from_speech_synthesizer(self.speech_synthesizer)
        connection.open(True)

    def speech_synthesis(self, txt):
        # The ssml string synthesize
        speech_synthesis_result = self.speech_synthesizer.speak_ssml_async(self.generate_ssml(txt)).get()

        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioStarted:
            log.debug("Speech synthesizing for text [{}]".format(txt))
        elif speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            first_byte_latency = int(speech_synthesis_result.properties.get_property(speechsdk.PropertyId.SpeechServiceResponse_SynthesisFirstByteLatencyMs))
            log.debug(constant.latency_log.format(self.speech_synthesis.__name__, first_byte_latency))
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            log.warning("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    log.exception("Error details: {}".format(cancellation_details.error_details))
                    log.exception("Did you set the speech resource key and region values?")

    def generate_ssml(self, txt):
        constant.token_replace_mapping[constant.text_token] = txt
        ssml = self.ssml_string
        for token, value in constant.token_replace_mapping.items():
            ssml = ssml.replace(token, value)

        log.debug(ssml)
        return ssml
