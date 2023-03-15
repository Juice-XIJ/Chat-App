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
        self.prompt = [{'role': 'system', 'content': self.bot_description}]
        if self.total_tokens >= constant.token_limitation - constant.max_token:
            raise Exception('Description is too long. {} vs {}'.format(self.total_tokens, constant.token_limitation - constant.max_token))

    def chat(self, txt):
        start = time.time()
        self.prompt_processing(txt, False)
        completion = openai.ChatCompletion.create(
            model=constant.model_engine,
            messages=self.prompt,
            temperature=0.9,
            max_tokens=constant.max_token,
            top_p=0.1,
            frequency_penalty=0.5,
            presence_penalty=1,
            stream=True
        )

        response = ''
        first = True
        for event in completion:
            log.debug(event.choices[0].delta)

            if not event.choices[0].delta:
                log.info('\n', extra={'append': True})
            elif 'content' in event.choices[0].delta:
                response += event.choices[0].delta.content
                if first:
                    log.info('{}: {}'.format(constant.ai_name, response))
                    first = False
                else:
                    log.info(event.choices[0].delta.content, extra={'append': True})

        self.prompt_processing(response, True)
        end = time.time()
        log.debug(constant.latency_log.format(self.chat.__name__, (end - start) * 1000))
        return response

    def clean(self):
        self.prompt = [{'role': 'system', 'content': self.bot_description}]

    def get_rough_token_number(self, txt):
        return math.ceil(len(txt) / 2)

    def prompt_processing(self, new_txt, is_response):
        if is_response:
            self.prompt.append({'role': 'user', 'content': new_txt})
        else:
            self.prompt.append({'role': 'assistant', 'content': new_txt})

        self.total_tokens += self.get_rough_token_number(new_txt)
        while self.total_tokens >= constant.token_limitation - constant.max_token:
            removed = self.prompt.pop(1)
            self.total_tokens -= self.get_rough_token_number(removed)
