import uuid
from django.db import models


class Library(models.Model):
    port = models.IntegerField()
    url = models.CharField(max_length=255)
    proj = models.CharField(max_length=255)
    active = models.BooleanField(default=False)
    desc = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'library'

    def __str__(self):
        return self.opcode


class TaskLog(models.Model):
    username = models.CharField(max_length=255)
    opcode = models.CharField(max_length=255)
    source = models.CharField(max_length=255, default="server")
    code = models.IntegerField(default=0)
    desc = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'taskLog'

    def __str__(self):
        return self.opcode


class Project(models.Model):
    projectName = models.CharField(max_length=255)
    port = models.CharField(max_length=255)
    principal = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    mail = models.CharField(max_length=255)
    active = models.BooleanField()
    desc = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'project'

    def __str__(self):
        return self.operation
