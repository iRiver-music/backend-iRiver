from django.db import models
from User.models import Profile


class ActivityLog(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    log_type = models.CharField(max_length=20, choices=[
        ('comment', 'Comment'),
        ('error', 'Error'),
    ])

    def __str__(self):
        return f"{self.profile.user.username} - {self.created_at} - {self.log_type}"
