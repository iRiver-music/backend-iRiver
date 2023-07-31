import re
from django.db import models


class Album(models.Model):
    artist = models.CharField(max_length=100, unique=True)
    desc = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

    def clean(self):
        # 定義需要過濾的特殊字元的正則表達式
        # 這裡示範過濾 emoji 和非法字元
        emoji_pattern = re.compile(
            r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+')
        illegal_chars_pattern = re.compile(r'[^\u0000-\uFFFF]+')

        # 過濾 artist 欄位
        if self.artist:
            self.artist = emoji_pattern.sub('', self.artist)
            self.artist = illegal_chars_pattern.sub('', self.artist)

        # 過濾其他需要過濾的欄位，以此類推

    def save(self, *args, **kwargs):
        self.clean()  # 在保存數據前先進行過濾
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'Music'
        db_table = 'album'

    def __str__(self):
        return self.title


class Artist(models.Model):
    artist = models.CharField(max_length=255, unique=True)
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # 定義需要過濾的特殊字元的正則表達式
        # 這裡示範過濾 emoji 和非法字元
        emoji_pattern = re.compile(
            r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+')
        illegal_chars_pattern = re.compile(r'[^\u0000-\uFFFF]+')

        # 過濾 artist 欄位
        if self.artist:
            self.artist = emoji_pattern.sub('', self.artist)
            self.artist = illegal_chars_pattern.sub('', self.artist)

    class Meta:
        app_label = 'Music'
        db_table = 'artists'

    def __str__(self):
        return self.artist


class Song(models.Model):
    artist = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    music_ID = models.CharField(max_length=255, unique=True)
    album = models.CharField(max_length=255, default="null")
    label = models.CharField(max_length=255, default="null")
    artist_url = models.CharField(max_length=255, default="null")
    sources = models.CharField(max_length=255, default="loaction")
    download_status = models.BooleanField(default=False)
    style = models.CharField(max_length=255, default="null")
    country = models.CharField(max_length=255, default="null")
    language = models.CharField(max_length=255, default="null")
    description = models.CharField(max_length=255, default="null")
    keywords = models.CharField(max_length=255, default="null")
    ch_lyrics = models.TextField(default="null")
    en_lyrics = models.TextField(default="null")
    rating = models.CharField(max_length=255, default="null")
    views = models.IntegerField(default=0)
    release_year = models.IntegerField(default=0)
    publish_time = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # 定義需要過濾的特殊字元的正則表達式
        # 這裡示範過濾 emoji 和非法字元
        emoji_pattern = re.compile(
            r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+')
        illegal_chars_pattern = re.compile(r'[^\u0000-\uFFFF]+')

        # 過濾 title 欄位
        if self.title:
            self.title = emoji_pattern.sub('', self.title)
            self.title = illegal_chars_pattern.sub('', self.title)
          # 過濾 artist 欄位
        if self.artist:
            self.artist = emoji_pattern.sub('', self.artist)
            self.artist = illegal_chars_pattern.sub('', self.artist)

        # 過濾其他需要過濾的欄位，以此類推

    def save(self, *args, **kwargs):
        self.clean()  # 在保存數據前先進行過濾
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'Music'
        db_table = 'songs'

    # def save(self, *args, **kwargs):
    #     existing_song = Song.objects.using(
    #         'test').filter(music_ID=self.music_ID).first()
    #     if existing_song:
    #         ret

    def __str__(self):
        return self.music_ID


class Style(models.Model):
    artist = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    music_ID = models.CharField(max_length=255)
    album = models.CharField(max_length=255, default="null")
    label = models.CharField(max_length=255, default="null")
    artist_url = models.CharField(max_length=255, default="null")
    sources = models.CharField(max_length=255, default="loaction")
    download_status = models.BooleanField(default=False)
    style = models.CharField(max_length=255, default="null")
    country = models.CharField(max_length=255, default="null")
    language = models.CharField(max_length=255, default="null")
    description = models.CharField(max_length=255, default="null")
    keywords = models.CharField(max_length=255, default="null")
    ch_lyrics = models.TextField(default="null")
    en_lyrics = models.TextField(default="null")
    rating = models.CharField(max_length=255, default="null")
    views = models.IntegerField(default=0)
    release_year = models.IntegerField(default=0)
    publish_time = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # 定義需要過濾的特殊字元的正則表達式
        # 這裡示範過濾 emoji 和非法字元
        emoji_pattern = re.compile(
            r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+')
        illegal_chars_pattern = re.compile(r'[^\u0000-\uFFFF]+')

        # 過濾 title 欄位
        if self.title:
            self.title = emoji_pattern.sub('', self.title)
            self.title = illegal_chars_pattern.sub('', self.title)
          # 過濾 artist 欄位
        if self.artist:
            self.artist = emoji_pattern.sub('', self.artist)
            self.artist = illegal_chars_pattern.sub('', self.artist)

        # 過濾其他需要過濾的欄位，以此類推

    def save(self, *args, **kwargs):
        self.clean()  # 在保存數據前先進行過濾
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'Music'
        db_table = 'style'

    def __str__(self):
        return self.artist


class StyleTitle(models.Model):
    title = models.CharField(max_length=255)
    style = models.CharField(max_length=255, default="null")
    desc = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.clean()  # 在保存數據前先進行過濾
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'Music'
        db_table = 'styleTitle'

    def __str__(self):
        return self.title


class DowARtist(models.Model):
    artist = models.CharField(max_length=255, unique=True)
    artist_url = models.CharField(max_length=255)
    artist_img_url = models.CharField(max_length=255)

    # 是不是暫存的
    style = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # 定義需要過濾的特殊字元的正則表達式
        # 這裡示範過濾 emoji 和非法字元
        emoji_pattern = re.compile(
            r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+')
        illegal_chars_pattern = re.compile(r'[^\u0000-\uFFFF]+')

        # 過濾 artist 欄位
        if self.artist:
            self.artist = emoji_pattern.sub('', self.artist)
            self.artist = illegal_chars_pattern.sub('', self.artist)

    def save(self, *args, **kwargs):
        self.clean()  # 在保存數據前先進行過濾
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'Music'
        db_table = 'dow'

    def __str__(self):
        return self.artist
