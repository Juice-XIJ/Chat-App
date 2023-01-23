import os
import json

# ==== repo path
root_path = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join("resources", "config.json"), 'r') as f:
    config = json.load(f)


# ==== Supported languages: en-us, zh-cn
supported_language = ['en-us', 'zh-cn']
language_index = 1
language = supported_language[language_index]


# ==== speech service info. Create Azure Speech Resources:
# https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-speech-to-text?tabs=windows%2Cterminal&pivots=programming-language-python#prerequisites
# Please make sure your region is compatible with tts voice name is in this list (some preview voice names are only supported in part of regions):
# https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support?tabs=tts
# In resources/tts.config, tts_voice.json listed all available languages/voice/style in region eastus
api_key = config['speech_resources']['api_key']
region = config['speech_resources']['region']


# ==== key word detection meta
supported_hello_keyword = ['hey blue', '胖胖你好']
hello_keyword = supported_hello_keyword[language_index]

supported_bye_keyword = ['bye bye blue', '再见']
bye_keyword = supported_bye_keyword[language_index]

hello_key_word_model_list = ['advanced_en_us_hello.table', 'basic_zh_cn_hello.table']
hello_key_word_model = os.path.join('resources', 'key_word_models', hello_key_word_model_list[language_index])

bye_key_word_model_list = ['basic_en_us_bye.table', 'basic_zh_cn_bye.table']
bye_key_word_model = os.path.join('resources', 'key_word_models', bye_key_word_model_list[language_index])

hello_audio_list = ['en_us_hello.wav', 'zh_ch_hello_0.wav']
hello_audio = os.path.join('resources', hello_audio_list[language_index])


# ==== open ai - chatgpt info. Create OpenAi account and api key: https://beta.openai.com/account/api-keys
openai_key = config['openai']['api_key']
bot_character = '{0} is a cute girl that is friendly:'
ai_name_list = ['blue', '胖胖']
ai_name = ai_name_list[language_index]
model_engine_list = ['text-ada-001', 'text-babbage-001	', 'text-curie-001', 'text-davinci-003']
model_engine = model_engine_list[3]  # most powerful engine


# ==== tts info
# In resources/tts.config, tts_voice.json listed all available languages/voice/style in region eastus. If style not existed, just leave it as ''
# or you can visit
#   https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/rest-text-to-speech?tabs=streaming#sample-request
# to get full list in your region
lang_list = ['en-us', 'zh-cn']
tts_lang = lang_list[language_index]
voice_name_list = ['en-US-JennyNeural', 'zh-CN-XiaohanNeural']
voice_name = voice_name_list[language_index]

style_list = ['friendly', 'affectionate']
style = style_list[language_index]
styledegree_list = ['1', '1']
styledegree = styledegree_list[language_index]

role_list = ['', 'YoungAdultFemale']
role = role_list[language_index]

hello_word_list = ['Hey I\'m here', '你好呀']
hello_word = hello_word_list[language_index]

lang_token = '[lang]'
voice_name_token = '[name]'
style_token = '[style]'
styledegree_token = '[styledegree]'
text_token = '[text]'
role_token = '[role]'

token_replace_mapping = {
    lang_token: tts_lang,
    voice_name_token: voice_name,
    style_token: style,
    styledegree_token: styledegree,
    text_token: '',
    role_token: role
}


# ==== latency log format: [Latency] [function name] [latency in ms]
latency_log = '[Latency] [{}] [{:.0f}ms]'
