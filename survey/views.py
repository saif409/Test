from django.db import DatabaseError, transaction
from django.shortcuts import render,get_object_or_404,redirect
from .forms import QuestionCreationForm, SurveyCreationForm, QuestionFormset, AddressCreationForm,SurveyorAssigningForm
from .models import Survey, Question,AnsType
from sadmin.models import Area
from django.core.paginator import Paginator
from django.forms import formset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


@transaction.atomic
def add_survey(request):
    if request.user.is_authenticated:
        form = SurveyCreationForm()
        address_form = AddressCreationForm()
        if request.method == 'POST':
            form = SurveyCreationForm(request.POST)
            form.question_instances = QuestionFormset(request.POST)

            address = {
                'country': request.POST.get('country', None),
                'division': request.POST.get('state', None),
                'district': request.POST.get('district', None),
                'subdistrict': request.POST.get('subdistrict', None),
                'area_name': request.POST.get('area', None),
            }
            survey_address = AddressCreationForm(address)

            survey = None
            if form.is_valid():
                survey = Survey(**form.cleaned_data)
                survey.save()
            if form.question_instances.is_valid():
                if form.question_instances.cleaned_data is not None:

                    for item in form.question_instances.cleaned_data:
                        question = Question(**item)
                        question.save()
                        survey.question.add(question)

            if survey_address.is_valid():
                survey_address = Area(**survey_address.cleaned_data)
                try:
                    survey_address.save()
                except DatabaseError as e:
                    print(e)
                    raise DatabaseError(e)
                survey.area = survey_address
                survey.save()
                messages.success(request, 'Survey Created Successfully!')
        context = {'form': form, 'address_form': address_form, 'isact_createsurvey': 'active'}
        return render(request, 'sadmin_templates/survey/create_survey.html', context)
    else:
        return redirect('admin_login')

def survey_list(request):
    if request.user.is_authenticated:
        all_survey = Survey.objects.all()[::-1]
        paginator = Paginator(all_survey, 100)
        page = request.GET.get('page', )
        all_skrillsignups = paginator.get_page(page)

        context = {
            "all_survey": all_skrillsignups,
            'isact_surveylist': 'active'
        }
        return render(request, 'sadmin_templates/survey/survey_list.html', context)
    else:
        return redirect('admin_login')



def assign_surveyor(request, id):
    if request.user.is_authenticated:
        survey_obj = get_object_or_404(Survey, id=id)
        survey_user_obj = survey_obj.survey_user.all()
        survey = Survey.objects.get(pk=id)
        SurveyerFormSet = formset_factory(SurveyorAssigningForm)
        form = SurveyerFormSet()
        txt = ''
        if request.method == 'POST':
            form.surveyor_instances = SurveyerFormSet(request.POST)
            if form.surveyor_instances.is_valid():
                if form.surveyor_instances.cleaned_data is not None:
                    for item in form.surveyor_instances.cleaned_data:
                        if len(item) > 0:
                            survey.survey_user.add(item['Select_Username'])
                            txt = 'Assigned Successfully!'
                        else:
                            txt = 'Error! Select Please!'

                messages.success(request, txt)
        context = {
            'survey': survey,
            'form': form,
            'survey_obj':survey_obj,
            'survey_user':survey_user_obj,
            'isact_surveylist': 'active',

        }
        return render(request, 'sadmin_templates/survey/assign_surveyor.html', context)
    else:
        return redirect('admin_login')



def survey_delete(request, pid):
    if request.user.is_authenticated:
        post = get_object_or_404(Survey, id=pid)
        post.delete()
        messages.warning(request, 'Deleted successfully!')
        return redirect('survey_list')
    else:
        return redirect('admin_login')


def survey_update(request,id):
    if request.user.is_authenticated:
        survey_obj = get_object_or_404(Survey, id=id)
        survey_user_obj = survey_obj.survey_user.all()
        survey_question_obj = survey_obj.question.all()
        if request.method == "POST":
            survey_obj.title=request.POST.get('title')
            survey_obj.save()
            messages.success(request, 'Updated Successfully!')

        context = {
            'get_survey': survey_obj,
            'isact_surveylist': 'active',
            'survey_users': survey_user_obj,
            'survey_question': survey_question_obj
        }
        return render(request, 'sadmin_templates/survey/update_survey.html',context)


def view_survey(request,id):
    if request.user.is_authenticated:
        survey_obj = get_object_or_404(Survey, id=id)
        survey_user_obj = survey_obj.survey_user.all()
        survey_question_obj = survey_obj.question.all()
        context = {
            'get_survey': survey_obj,
            'isact_surveylist': 'active',
            'survey_users': survey_user_obj,
            'survey_question': survey_question_obj
        }
        return render(request, 'sadmin_templates/survey/view_survey.html', context)
    else:
        return redirect('admin_login')


def assigned_surveyor_remove(request, id, user_id):
    if request.user.is_authenticated:
        survey_obj = get_object_or_404(Survey, id=id)
        survey_user = survey_obj.survey_user.remove(user_id)
        messages.warning(request, 'Deleted Successfully!')
        return redirect('update_survey', id=id)
    else:
        return redirect('admin_login')


def assigned_question_remove(request, id, question_id):
    if request.user.is_authenticated:
        survey_obj = get_object_or_404(Survey, id=id)
        survey_question = survey_obj.question.remove(question_id)
        messages.warning(request, 'Deleted Successfully!')
        return redirect('update_survey', id=id)
    else:
        return redirect('admin_login')


def add_question(request,id):
    if request.user.is_authenticated:
        survey_obj = get_object_or_404(Survey, id=id)
        survey_question_obj = survey_obj.question.all()
        ans_type = AnsType.objects.all().distinct()
        if request.method == "POST":
            question = request.POST.get('question')
            answer_type = AnsType.objects.get(id=int(request.POST.get('answer_type')))
            answer_option = request.POST.get('answer_option')
            question_obj = Question(question_title=question, ans_type=answer_type, question_ans=answer_option)
            question_obj.save()
            survey_obj.question.add(question_obj)

            messages.success(request, 'Added Successfully!')
        context={
            "survey_obj": survey_obj,
            "survey_questions":survey_question_obj,
            'ans_type': ans_type,
            'isact_surveylist': 'active',
        }
        return render(request, 'sadmin_templates/survey/add_question.html', context)
    else:
        return redirect('admin_login')







