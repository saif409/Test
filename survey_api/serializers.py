from rest_framework import serializers
from survey.models import Question,Survey, Answer


class SurveySerializers(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class SurveyAnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['question', 'q_ans']


