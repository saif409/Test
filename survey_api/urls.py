from django.urls import path
from.views import SurveyAPIView,SurveyAPIDetailView, SurveyData, SurveyInsertView,UploadImages


urlpatterns = [
    # path('survey_list/<int:pk>/', SurveyAPIDetailView.as_view()),
    # path('survey/<int:pk>/',SurveyAPIView.as_view()),
    path('data/', SurveyData.as_view()),
    path('uploadimage/', UploadImages.as_view()),
]