from django.contrib import admin
from .models import AnsType, Survey, Question ,Answer, ImageData
# Register your models here.

admin.site.register(AnsType)
admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(ImageData)