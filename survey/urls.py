from django.urls import path, include
from . import views


urlpatterns = [
    path('create_survey/', views.add_survey, name='add_survey'),
    path('survey_list/', views.survey_list, name='survey_list'),
    path('assign_surveyor/<int:id>', views.assign_surveyor, name='assign_surveyor'),
    path('update_survey/<int:id>/', views.survey_update, name="update_survey"),
    path('delete_survey/<int:pid>/', views.survey_delete, name="delete_survey"),
    path('survey_view/<int:id>/', views.view_survey, name="survey_view"),
    path('remove_assigned_surveyor/<int:id>/<int:user_id>/', views.assigned_surveyor_remove, name="remove_assigned_surveyor"),
    path('remove_assigned_question/<int:id>/<int:question_id>/', views.assigned_question_remove, name="remove_assigned_question"),
    path('question_add/<int:id>', views.add_question,name="question_add")



]