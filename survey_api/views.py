from PIL import Image
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json
from survey.models import Answer, Question, ImageData

from survey.models import Question,Survey
from sadmin.models import Surveyor
from surveyapp.settings import BASE_DIR
from .serializers import SurveySerializers, SurveyAnsSerializer
from rest_framework.response import Response


class SurveyAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializers


class SurveyAPIView(generics.ListAPIView):
    http_method_names = ['get', 'post', 'put', 'delete']

    def get(self, request, pk):
        queryset = get_object_or_404(Survey, pk=pk)
        serializer_data = SurveySerializers(queryset)
        return Response(serializer_data.data)


def options_format(data):
    temp_list = []
    if len(data) > 0:
        # split string by ,
        chunks = data.split(',')
        return chunks
    return []


class SurveyData(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request, **kwargs):
        data_list = []
        surveyer_obj = request.user.surveyer
        surveyor_id = surveyer_obj.id

        survey_obj = Survey.objects.all().filter(survey_user=surveyor_id)
        for single_survey in survey_obj:
            survey_list = []
            temp_dict = {
                "id": single_survey.id,
                "title": single_survey.title,
                "survey_date": single_survey.survey_date,
                "area_id": single_survey.area.id,
                "survey_area": single_survey.area.address_format,
                "questions": []
            }
            for res in single_survey.question.all():
                temp_dict["questions"].append({
                    "id": res.id,
                    "title": res.question_title,
                    "view_type": res.ans_type.name,
                    "options": options_format(res.question_ans)

                })
            data_list.append(temp_dict)
        responses = {
            "Status": "success",
            "Error": {},
            "data": data_list
        }
        return Response(responses, status=200)

    def post(self, request, **kwargs):
        created_at = request.data.get('created_at')
        updated_at = request.data.get('updated_at')
        survey_id = request.data.get('survey_id')
        # survey_count = request.data.get('survey_count')
        lat_lon = request.data.get('lat_lon')

        user_ans = Answer.objects.all().filter(user=request.user).annotate(counter=Max("count_id")).order_by("-counter").first()
        if user_ans is not None:
            survey_count = user_ans.count_id +1
        else:
            survey_count = 1


        data_list = []
        for val in request.data.get('ans'):

            data_dict = {
                "created_at": str(created_at),
                "updated_at": str(updated_at),
                "survey_id": survey_id,
                "survey_count": survey_count,
                "lat_lon": lat_lon,
                "question": Question.objects.get(id=val['question']),
                "q_ans": val['q_ans']
            }
            data_list.append(data_dict)

        for data in data_list:
            ans = Answer(created_at=data['created_at'], updated_at=data['updated_at'], survey_id=data['survey_id'], lat_lon=data['lat_lon'], count_id=data['survey_count'], question=data['question'], q_ans=data['q_ans'],user=request.user)
            ans.save()

        responses = {
            "Status": "success",
            "Error": '',
        }
        return Response(responses, status=200)


class SurveyInsertView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    serializer_class = SurveyAnsSerializer


class UploadImages(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request, *args, **kwargs):
        host = "{}".format(request.META['HTTP_HOST'])

        image = request.FILES['image']
        file_name = str(request.FILES['image'])
        if file_name:
            tmp_ = file_name.split('.')[0]

            tmp_ = tmp_.split('_')

            survey_id, question_id, surveyor_id, milis = int(tmp_[0]), int(tmp_[1]), int(tmp_[2]), tmp_[3]
            survey = Survey.objects.get(id=survey_id)
            surveyor = Surveyor.objects.get(id=surveyor_id)
            question = Question.objects.get(id=question_id)
            url = '/images/' + file_name
            img_data = ImageData(survey=survey, question=question, surveyor=surveyor, milis=milis, url=url)
            img_data.save()

        if image:
            image = Image.open(image)
            if image.mode is not 'RGB':
                image = image.convert('RGB')
            image.save(BASE_DIR + '/static/images/{}'.format(file_name), 'JPEG')
            responses = {
                "Status": "success",
                "imageUrl": 'http://'+host+'/images/' + file_name,
                "Error": '',
            }
            return Response(responses, status=200)
        else:
            return Response({"Status": "fail"})

