import glob
import json
import os
import re
from django.conf import settings
from pytube import YouTube

from lib.clear_str import process_artist, process_title
from Music.models import DowARtist, StyleTitle, Style


# main =================================================

def clean_style():
    DowARtist.objects.all().delete()
    StyleTitle.objects.all().delete()
    Style.objects.all().delete()
    pass


def push_style():
    json_folder = os.path.join(settings.BASE_DIR, 'Json', 'style')
    json_files = glob.glob(os.path.join(json_folder, '*.json'))

    print(json_files)

    for file in json_files:
        with open(file, 'r') as file:
            file_content = file.read()
            hadle_data(data=json.loads(file_content))


def hadle_data(data):
    # 遍歷資料
    for albumSet in data:
        url = "https://www.youtube.com" + albumSet["Link"]
        obj = YouTube(url=url)
        # keywords
        music_ID = get_music_ID(url=url)

        artist = process_artist(artist=obj.author)
        title = process_title(title=obj.title, artist=obj.author)
        print(artist, "   ", title)
        # push style

        if not StyleTitle.objects.filter(title=albumSet["albumSuperSetTitle"], style=albumSet["Album"]).exists():
            StyleTitle.objects.create(
                title=albumSet["albumSuperSetTitle"], style=albumSet["Album"], desc=albumSet["Description"], name=albumSet['Album'])

        if not Style.objects.filter(music_ID=music_ID, style=albumSet["Album"]).exists():
            Style.objects.create(
                artist=artist, title=title, music_ID=music_ID, style=albumSet["Album"])

        # dow all song

        if not DowARtist.objects.filter(artist=artist).exists():
            DowARtist.objects.create(
                artist=artist, artist_url=obj.channel_url, artist_img_url=obj.thumbnail_url,
                style=True)


def get_music_ID(url: str) -> str:
    match = re.search(r'(?<=v=)[^&]+', url)
    if match:
        music_ID = match.group(0)[-11:]
    else:
        music_ID = re.search(
            r"shorts\/(\w{11})", url).group(1)

    return music_ID


def creat_style(music_ID, albumSet):
    #  push to style and styleTitle
    if StyleTitle.objects.filter(title=albumSet["albumSuperSetTitle"], style=albumSet["Album"]).count() == 0:
        StyleTitle.objects.create(
            title=albumSet["albumSuperSetTitle"], style=albumSet["Album"], desc=albumSet["Description"], name=albumSet['Album'])

    if Style.objects.filter(music_ID=music_ID, style=albumSet["Album"]).count() == 0:
        Style.objects.create(
            artist=albumSet["Artist"], title=albumSet["Name"], music_ID=music_ID, style=albumSet["Album"])
