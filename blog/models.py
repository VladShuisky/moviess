from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

class CustomUser(AbstractUser):
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.username

class Post(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    draft = models.BooleanField(default=False)
    author = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)

    def date(self):
        date = self.pub_date.date()
        time = self.pub_date.time()
        return f'{date} в {time.hour}:{time.minute}'


    def __str__(self):
        return f'{self.title} -- {self.text[:20]}... |||(Создано {self.date()})'



