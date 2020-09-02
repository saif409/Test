"""surveyapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from.import views

urlpatterns = [
    path('', views.admin_login, name="admin_login"),
    path('logout/', views.admin_logout, name="admin_logout"),
    path('home/', views.admin_home, name="admin_home"),
    path('surveyor_register/', views.register_surveyor, name="surveyor_register"),
    path('surveyor_list/<str:filter>/', views.surveyor_list, name="surveyor_list"),
    path('surveyor_update/<int:pid>/', views.update_surveyor, name="surveyor_update"),
    path('surveyor_view/<int:id>/', views.view_surveyor, name="surveyor_view"),
    path('delete_surveyor/<int:pid>/', views.surveyor_delete, name="delete_surveyor"),
    path('view_survey_answer/<int:id>', views.survey_answer, name='view_survey_answer'),

    path('add_country/', views.country_add , name="add_country"),
    path('update_country/<int:id>/', views.country_update, name="update_country"),
    path('remove_country/<int:id>/', views.delete_country, name="remove_country"),

    path('add_division/', views.division_add, name="add_division"),
    path('update_division/<int:id>/', views.division_update, name="update_division"),
    path('remove_division/<int:id>/', views.delete_division, name="remove_division"),

    path('district_add/', views.district_add, name="district_add"),
    path('update_district/<int:id>/', views.district_update, name="update_district"),
    path('remove_district/<int:id>/', views.delete_district, name="remove_district"),

    path('add_sub_district/', views.sub_district_add, name="add_sub_district"),
    path('update_sub_district/<int:id>/', views.sub_district_update, name="update_sub_district"),
    path('remove_sub_district/<int:id>/', views.delete_sub_district, name="remove_sub_district"),

    path('add_answer_type/', views.answer_type_add, name="add_answer_type"),
    path('update_answer_type/<int:id>/', views.answer_type_update, name="update_answer_type"),
    path('remove_answer_type/<int:id>/', views.delete_answer_type, name="remove_answer_type"),




]
