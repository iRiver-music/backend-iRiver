
import re


# artist =================================================================

def remove_special_characters(text):
    # 定义一个正则表达式模式，用于匹配特殊字符
    pattern = r'[!@#$%^&*()_+{}\[\]:;<>,.?\\\/|`~\'"\-=]'

    # 使用 re.sub() 函数将特殊字符替换为空字符串
    cleaned_text = re.sub(pattern, '', text)

    return cleaned_text


def process_artist(artist):
    artist = artist.strip()  # Remove leading and trailing spaces
    # artist = artist.lower()

    artist = delete_tag(artist)

    artist = re.sub(r'\\/', '', artist)

    artist = re.sub(r'\s+', '', artist)  # Remove spaces

    artist = remove_special_characters(artist)

    artist = re.sub(r' ', '', artist)

    return artist


# title =================================================================


def process_title(title, artist):
    title = title.strip()  # Remove leading and trailing spaces
    # title = title.lower()
    title = re.sub(r'/', '', title)
    title = re.sub(r'’', '', title)

    # Remove specific words and symbols
    title = re.sub(r'主題|歌|《純粹中翻》|中日詞|電影', '', title, flags=re.IGNORECASE)
    title = re.sub(f'{artist}', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s*-\s*', '', title)
    title = re.sub(r'[=.#、：\/\[\]－—―–()\|\｜@「」]', '', title)
    title = re.sub(
        r'\(.*?mv.*?\)|\[.*?官方.*?\]|（.*?Cover.*?）|\[.*?中.*?\]||\「.*?中.*?\」|\(.*?from.*?\)', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\(\s*\)|（\s*）', '', title)
    title = re.sub(r'\【\s*\】|（\s*）', '', title)
    title = re.sub(r'＜.*?＞', '', title)
    title = re.sub(r'\【中\】', '', title)
    title = re.sub(r'\【動態\】', '', title)
    title = re.sub(r'\b\d{4}\b|\b\d{1,2}/\d{1,2}\b', '', title).strip()
    title = re.sub(r'\d{5,}', '', title)

    # Remove years from the title
    pattern = r'\d{4}'
    title = re.sub(pattern, '', title)

    # Remove artist name from the title
    artist_escaped = re.escape(artist)
    artist_regex = re.compile(artist_escaped, flags=re.IGNORECASE)
    title = artist_regex.sub("", title)

    # Remove tags from the title
    title = delete_tag(title)
    # title = title.rstrip()

    title = remove_special_characters(title)
    return title


def delete_tag(name):
    return re.sub(r'official|music|video|Audio|demo|Acoustic|version|MV|HD|Remix|live|4k|cover|OP|OfficialYouTubeChannel|Feat|EP|OST|Deluxe|Part|Lyric', '', name, flags=re.IGNORECASE)
