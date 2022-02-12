import markovify
import MeCab
import re
import unicodedata

def format_text(t):
    t = t.replace('　', ' ')  # Full width spaces
    # t = re.sub(r'([。．！？…]+)', r'\1\n', t)  # \n after ！？
    t = re.sub(r'(.+。) (.+。)', r'\1 \2\n', t)
    t = re.sub(r'\n +', '\n', t)  # Spaces
    t = re.sub(r'([。．！？…])\n」', r'\1」 \n', t)  # \n before 」
    t = re.sub(r'\n +', '\n', t)  # Spaces
    t = re.sub(r'\n+', r'\n', t).rstrip('\n')  # Empty lines
    t = re.sub(r'\n +', '\n', t)  # Spaces
    return t

def join_diacritic(text, mode="NFC"):
    """
    基底文字と濁点・半濁点を結合
    """
    # str -> bytes
    bytes_text = text.encode()

    # 濁点Unicode結合文字置換
    bytes_text = re.sub(b"\xe3\x82\x9b", b'\xe3\x82\x99', bytes_text)
    bytes_text = re.sub(b"\xef\xbe\x9e", b'\xe3\x82\x99', bytes_text)

    # 半濁点Unicode結合文字置換
    bytes_text = re.sub(b"\xe3\x82\x9c", b'\xe3\x82\x9a', bytes_text)
    bytes_text = re.sub(b"\xef\xbe\x9f", b'\xe3\x82\x9a', bytes_text)

    # bytet -> str
    text = bytes_text.decode()

    # 正規化
    text = unicodedata.normalize(mode, text)

    return text

text_file = open('input.txt', 'r', encoding='utf8')
text = text_file.read()

parsedLines = []

for line in text.splitlines():
    t = format_text(line)
    t = join_diacritic(t) # 濁点がおかしいので正常な文字列に変換する
    parsedLines.append(MeCab.Tagger('-Owakati').parse(t))

parsed_text = '\n'.join(parsedLines)

model = markovify.NewlineText(parsed_text, state_size=2, well_formed=True)

with open('model.json', 'w', encoding='utf8') as f:
    f.write(model.to_json())