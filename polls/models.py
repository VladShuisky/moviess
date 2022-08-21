from secrets import choice
from statistics import mode
from django.db import models
from django.utils import timezone
import datetime

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date_published')

    def __str__(self):
        return f'{self.question_text}: {self.pub_date}'

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def last_month(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=30)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    draft = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.choice_text}'