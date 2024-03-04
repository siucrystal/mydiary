from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.db.models.fields.related import ManyToManyField

from datetime import datetime

class CreateDiary(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_diary')
    diary_id = models.AutoField(primary_key=True)
    date = models.CharField(max_length=30,blank=True,null=True)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(blank=True, null=True)
    weather = models.CharField(max_length=30)
    mood = models.CharField(max_length=30)
    title = models.CharField(max_length=200)
    content = models.TextField()
    photo = models.ImageField(blank=True,null=True, upload_to='diary_photo/')
    reflection = models.CharField(max_length=200, blank=True, null=True)
    voter = models.ManyToManyField(User, related_name='voter_diary')
    praise = models.CharField(max_length=200, blank=True, null=True)
    disclose_choice= (
        ('public', '공개'),
        ('private', '비공개'),
    )
    disclose = models.CharField(max_length=20, choices=disclose_choice, default='public')

    def __str__(self):
        return self.title

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(CreateDiary, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(blank=True, null=True)