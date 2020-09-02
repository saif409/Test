from django import forms
from django.forms.formsets import formset_factory
from .models import Survey, AnsType
from sadmin.models import Area,Surveyor
from django.forms import TextInput


class AddressCreationForm(forms.ModelForm):
    class Meta:
        model = Area
        exclude = ()


class QuestionCreationForm(forms.Form):
    question_title = forms.CharField( widget=forms.TextInput(attrs={'class': 'form-control'}))
    ans_type = forms.ModelChoiceField(required=True,
                                      queryset=AnsType.objects.all().order_by('name'), initial=1,
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    question_ans = forms.CharField(required=False, max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))


QuestionFormset = formset_factory(QuestionCreationForm)


class SurveyCreationForm(forms.ModelForm):
    question = QuestionFormset()
    title = forms.CharField(required=True)

    class Meta:
        model = Survey
        exclude = ('title', 'question', 'area', 'survey_user')



class SurveyorAssigningForm(forms.Form):
    Select_Username = forms.ModelChoiceField(required=True,queryset=Surveyor.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))


class SurveyUpdateForm(forms.ModelForm):
    question = QuestionFormset()

    class Meta:
        model = Survey
        exclude = ('question', 'area', 'survey_user')