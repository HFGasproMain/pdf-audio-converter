from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone_number = models.IntegerField(null=True)
    photo = models.ImageField(upload_to='users', default='default.jpeg', blank=True)
    location = models.CharField(max_length=60, default='Lagos')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=60, null=True)
    pdf_file = models.FileField(upload_to='pdf_files')
    #audio_file = models.FileField(upload_to='audio/%Y/%m/%d/', null=True, blank=True)
    audio_file = models.FileField(upload_to='audio_files', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pdf_file.name

    class Meta:
        ordering = ('-created_at',)



LANGUAGE_CHOICES = [
    ('en', 'English'),
    ('es', 'Spanish'),
    ('fr', 'French'),
    # Add more language choices as needed
]