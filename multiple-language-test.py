from gtts.lang import tts_langs

langs = tts_langs()
for code, name in langs.items():
    print(f"{code}: {name}")
