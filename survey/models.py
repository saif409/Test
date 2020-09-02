from django.db import models
from sadmin.models import Country, Division, District, SubDistrict, Area,Surveyor
from django.contrib.auth.models import User
# Create your models here.


class AnsType(models.Model):
    name = models.CharField(max_length=25,unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    question_title = models.CharField(max_length=256, null=True, blank=True)
    ans_type = models.ForeignKey(AnsType, on_delete=models.SET_NULL, null=True, blank=True)
    question_ans = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.question_title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING, null=True, blank=True)
    q_ans = models.TextField()
    survey_id = models.IntegerField()
    count_id = models.IntegerField()
    created_at = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.CharField(max_length=200, null=True, blank=True)
    lat_lon = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.question.question_title


class Survey(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True)
    question = models.ManyToManyField(Question, related_name="survey_question")
    area = models.ForeignKey(Area, on_delete=models.DO_NOTHING, null=True, blank=True)
    survey_user = models.ManyToManyField(Surveyor, related_name='survey_user')
    survey_date = models.DateField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.title


class ImageData(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.SET_NULL, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True)
    surveyor = models.ForeignKey(Surveyor, on_delete=models.SET_NULL, null=True, blank=True)
    milis = models.CharField(max_length=200)
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.url