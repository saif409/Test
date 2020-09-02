
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as rest_framework_view
from .custom_token import CustomAuthToken
urlpatterns = [
    path('api-token-auth/', rest_framework_view.obtain_auth_token),
    path('token/', CustomAuthToken.as_view()),
    path('admin/', admin.site.urls),
    path('',(include("sadmin.urls"))),
    path('survey/', (include("survey.urls"))),
    path('api/', include('survey_api.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)