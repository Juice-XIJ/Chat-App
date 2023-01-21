import openai
import time
import constant
from logger import log


class chatgpt():
    def __init__(self):
        openai.api_key = constant.openai_key
        self.bot_description = constant.bot_character.format(constant.ai_name)
        self.prompt = [self.bot_description]

    def chat(self, txt):
        start = time.time()
        self.prompt.append(txt)
        completion = openai.Completion.create(
            model=constant.model_engine,
            prompt='\n'.join(self.prompt),
            temperature=0.9,
            max_tokens=200,
            top_p=0.1,
            frequency_penalty=0.5,
            presence_penalty=1
        )

        response = completion.choices[0].text.replace('\n', '')
        log.debug('{}: {}'.format(constant.ai_name, completion.choices[0].text))

        self.prompt.append(response)
        log.info('{}: {}'.format(constant.ai_name, response))
        end = time.time()
        log.debug(constant.latency_log.format(self.chat.__name__, (end - start) * 1000))
        return response

    def clean(self):
        self.prompt.clear()
        self.prompt.append(self.bot_description)
