# Chat App
Chat App allows people to chat with a BOT. But you could define everything you want for the BOT, like it's person.

## Service Dependencies
Chat App leverages the MS speech service (Key word detection, TTS, STT) and OpenAI (ChatGPT).
Therefore you have to create your own resources:
1. Create your own [MS Speech Resource](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-text-to-speech?tabs=windows%2Cterminal&pivots=programming-language-python#prerequisites). It has free level on speech resources so you can have a try.

2. [OpenAI ChatGPT](https://beta.openai.com/overview). Free trial available as well.

## How to Play with?
1. When you finished `Service Dependencies`, please update them on variables `api_key`, `region` and `openai_key` in file `resources/config.json`.
2. Then you could describe who you want to talk with. Update your description on variable `bot_character` in file `constant.py`
3. (Optional) Now it's ready to run. But if you want to have your own key word, play voice, or bot name, feel free to update `info` in file `constant.py`.
4. Feel free to explore more available options :)

## Useful Resource Link
1. For MS Speech Service, please check:
    - [Key word detection](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/keyword-recognition-overview)
    - [Text-to-Speech](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/text-to-speech)
    - [Speech-to-Text](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-to-text)
    - [Speech Studio](https://speech.microsoft.com/portal)

2. [OpenAI ChatGPT](https://beta.openai.com/overview)