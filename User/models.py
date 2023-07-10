import datetime
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxLengthValidator

#國家清單
country=(
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
gender=(
    ('U','不透露'),
    ('M','男'),
    ('F','女'),
)

class login(models.Model):
    pass