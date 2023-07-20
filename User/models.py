import datetime
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxLengthValidator
from django.core.validators import MinValueValidator, MaxValueValidator

#國家清單
COUNTRY_CHOICES=(
    ('NN','不透露'),
    ('US','United States'),
    ('CA','Canada'),
    ('JP','Japan'),
    ('CN','China'),
    ('TW','Taiwan'),
    ('KR','Korea'),
    ('SG','Singapore'),
    ('MY','Malaysia'),
    ('TH','Thailand'),
    ('PH','Philippines'),
    ('ID','Indonesia'),
)
#性別清單
GENDER={
    ('U','不透露'),
    ('M','男'),
    ('F','女'),
}

# 登入
class Login(models.Model):
    email=models.CharField(max_length=255)
    username=models.CharField(max_length=255)
    password=models.CharField(max_length=255)

class Logingoogle(models.Model):
    provider=models.CharField(max_length=200,default="google") # 若未來新增其他的登入方式,如Facebook,GitHub...
    unique_id=models.CharField(max_length=200)
    user=models.ForeignKey(User,related_name="social",on_delete=models.CASCADE)

class Loginline(models.Model):
    pass

class Loginapple(models.Model):
    pass

# 設定
class Settings(models.Model):
    language=models.CharField(max_length=255)
    showmodal=models.CharField(max_length=255)
    audioquality=models.CharField(max_length=255)
    audioautoplay=models.CharField(max_length=255)
    wifiautodownload=models.CharField(max_length=255)

# 註冊
class Signup(models.Model):
    email=models.CharField(max_length=255)
    username=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    phone=models.CharField(max_length=255)
    gender=models.CharField(max_length=255)
    country=models.CharField(max_length=255)
    # gender=models.CharField(max_length=1,choices=GENDER)
    # country=models.CharField(max_length=2,choices=COUNTRY_CHOICES)
    birthday=models.DateField()
    # userimage=models.ImageField(upload_to='avatar/',default='avatar/default.png')

# 個人檔案
class Profile(models.Model):
    email=models.CharField(max_length=255)
    username=models.CharField(max_length=255)
    phone=models.CharField(max_length=255)
    gender=models.CharField(max_length=255)
    country=models.CharField(max_length=255)
    birthday=models.DateField()
    # userimage=models.ImageField(upload_to='avatar/',default='avatar/default.png')

# 回報問題
class Problem(models.Model):
    pass

class UserSocial(models.Model):
    userid = models.CharField(max_length=36, primary_key=True)
    email = models.CharField(max_length=24)
    uid = models.CharField(max_length=24)

class UserProfile(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    email = models.CharField(max_length=24)
    username = models.CharField(max_length=24)
    phone = models.CharField(max_length=16)
    country = models.CharField(max_length=2, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True)
    user_img_url = models.CharField(max_length=255, null=True, blank=True)
    test = models.BooleanField(default=False)
    level = models.PositiveSmallIntegerField(default=0)

class UserSettingEQ(models.Model):
    UID_EQ = models.CharField(max_length=36, primary_key=True)
    ENGANCE_HIGH = models.BooleanField(null=True, blank=True)
    ENGANCE_MIDDLE = models.BooleanField(null=True, blank=True)
    ENGANCE_LOW = models.BooleanField(null=True, blank=True)
    ENGANCE_HEAVY = models.BooleanField(null=True, blank=True)
    STYLE = models.CharField(max_length=255, null=True, blank=True)
    EQ_HIGH = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    EQ_MIDDLE = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    EQ_LOW = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    EQ_HEAVY = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    EQ_DISTORTION = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    EQ_ZIP = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    SPATIAL_AUDIO = models.CharField(max_length=255, null=True, blank=True)

class UserSetting(models.Model):
    UID_SETTING = models.CharField(max_length=36, primary_key=True)
    LANGUAGE = models.CharField(max_length=255)
    SHOW_MODAL = models.CharField(max_length=255)
    AUDIO_QUALITY = models.CharField(max_length=255)
    AUDIO_AUTO_PLAY = models.BooleanField()
    WIFI_AUTO_DOWNLOAD = models.BooleanField()
    CREATED_AT = models.DateTimeField(auto_now_add=True)