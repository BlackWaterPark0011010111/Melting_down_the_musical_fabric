from django.db import models
from django.contrib.auth.models import User

class MusicSheet(models.Model):
    title = models.CharField(max_length=100)
    pdf_file = models.FileField(upload_to='pdfs/')

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class ConversionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='pdfs/')
    converted_tabs = models.TextField()
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.date_uploaded}'
