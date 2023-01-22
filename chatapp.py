import string
from concurrent.futures import ThreadPoolExecutor

import constant
import key_word_detection
import openai_chatgtp
import stt
import tts
from logger import log

threadPool = ThreadPoolExecutor(max_workers=8, thread_name_prefix="chatapp")
key_word = key_word_detection.key_word_detection()
recognizer = stt.stt()
gpt = openai_chatgtp.chatgpt()
speaker = tts.tts()


def end_session_detection():
    key_word.bye_keyword_locally_from_microphone()
    key_word.stop_bye_keyword_recognition()


if __name__ == "__main__":
    try:
        key_word.hello_keyword_locally_from_microphone()
        key_word.stop_hello_keyword_recognition()

        speaker.speech_synthesis(constant.hello_word)

        session_stop = False
        empty_human_talk_count = 0
        human_talk = ''

        threadPool.submit(end_session_detection)
        while True:
            # end session when bye detected, or 5 empty human talk happened continuously, or bye keyword in human talk
            if key_word.is_bye_detected() \
                    or empty_human_talk_count > 5\
                    or constant.bye_keyword in human_talk.lower().translate(str.maketrans('', '', string.punctuation)):
                key_word.reset()
                break

            # get human talk
            human_talk = recognizer.recognize_from_microphone(empty_human_talk_count)

            if human_talk is None or len(human_talk) < 1:
                empty_human_talk_count = empty_human_talk_count + 1
            else:
                empty_human_talk_count = 0

                # get chatgpt response
                bot_response = gpt.chat(human_talk)
                speaker.speech_synthesis(bot_response)
    except BaseException as e:
        log.exception(e)
    finally:
        threadPool.shutdown(wait=False)
