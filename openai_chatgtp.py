import openai
import time
import constant
from logger import log
import math

class chatgpt():
    def __init__(self):
        openai.api_key = constant.openai_key
        self.bot_description = constant.bot_character.format(constant.ai_name)
        self.total_tokens = self.get_rough_token_number(self.bot_description)
        self.prompt = [self.bot_description]
        if self.total_tokens >= constant.token_limitation - constant.max_token:
            raise Exception('Description is too long. {} vs {}'.format(self.total_tokens, constant.token_limitation - constant.max_token))

    def chat(self, txt):
        start = time.time()
        self.prompt_processing(txt)
        completion = openai.Completion.create(
            model=constant.model_engine,
            prompt='\n'.join(self.prompt),
            temperature=0.9,
            max_tokens=constant.max_token,
            top_p=0.1,
            frequency_penalty=0.5,
            presence_penalty=1
        )

        response = completion.choices[0].text.replace('\n', '')
        log.debug('{}: {}'.format(constant.ai_name, completion.choices[0].text))

        self.prompt_processing(response)
        log.info('{}: {}'.format(constant.ai_name, response))
        end = time.time()
        log.debug(constant.latency_log.format(self.chat.__name__, (end - start) * 1000))
        return response

    def clean(self):
        self.prompt.clear()
        self.prompt.append(self.bot_description)

    def get_rough_token_number(self, txt):
        return math.ceil(len(txt) / 2)

    def prompt_processing(self, new_txt):
        self.prompt.append(new_txt)
        self.total_tokens += self.get_rough_token_number(new_txt)
        while self.total_tokens >= constant.token_limitation - constant.max_token:
            removed = self.prompt.pop(1)
            self.total_tokens -= self.get_rough_token_number(removed)
