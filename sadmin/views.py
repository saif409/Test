from django.contrib.auth.hashers import make_password
from django.shortcuts import render,get_object_or_404,redirect
from sadmin.models import Surveyor,Country,District,Division,SubDistrict
from survey.models import Survey,AnsType,Question,Answer
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator
from django.contrib.auth.models import User


def admin_home(request):
    if request.user.is_authenticated:
        total_survey_create = Survey.objects.all().count()
        total_surveyor_create = Surveyor.objects.all().count()
        total_surveyor_received = Answer.objects.all().count()
        total_question_created = Question.objects.all().count()

        survey = Survey.objects.all()[::-1]
        paginator = Paginator(survey, 10)

        page = request.GET.get('page', )
        all_survey = paginator.get_page(page)
        context={
            "total_survey_create":total_survey_create,
            "total_surveyor_create": total_surveyor_create,
            "total_surveyor_received":total_surveyor_received,
            "total_question_created":total_question_created,
            'isact_dashboard': 'active',
            'all_survey':all_survey
        }
        return render(request, 'sadmin_templates/admin_home.html',context)
    else:
        return redirect('admin_login')


def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_home')
    else:
        if request.method == "POST":
            user = request.POST.get('user', )
            password = request.POST.get('pass', )
            auth = authenticate(request, username=user, password=password)
            if auth is not None:
                login(request, auth)
                if request.user.is_superuser:
                    return redirect('admin_home')
                else:
                    messages.add_message(request, messages.ERROR, 'Please Login From Admin Account')
            else:
                messages.add_message(request, messages.ERROR, 'Username or password mismatch!')
    return render(request, 'sadmin_templates/login.html')



def admin_logout(request):
    logout(request)
    return redirect('admin_login')



def register_surveyor(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fname = request.POST.get('fname', )
            lname = request.POST.get('lname', )
            uname = request.POST.get('uname', )
            password = request.POST.get('password', )
            address = request.POST.get('adress', )
            country = request.POST.get('country', )
            division = request.POST.get('division', )
            district = request.POST.get('district', )
            subdistrict = request.POST.get('subdistrict', )
            area = request.POST.get('area', )
            designation = request.POST.get('designation', )
            phone= request.POST.get('phone', )
            email= request.POST.get('email', )
            user = User.objects.all().filter(username=uname)

            if user:
                messages.warning(request,"Data Collector Already Exists!")

            else:
                auth_info = {
                    'first_name': fname,
                    'last_name': lname,
                    'username': uname,
                    'password': make_password(password)
                }
                user = User(**auth_info)
                user.save()
                survey_user = Surveyor(user=user, email=email, address=address, division=division, district=district,
                                       country=country, sub_district=subdistrict, area=area, designation=designation,
                                       phone=phone)
                survey_user.save()
                messages.success(request, 'Created Successfully!')

        context = {
            'isact_registersurveyor': 'active',

        }
        return render(request, 'sadmin_templates/surveyor/register_surveyor.html',context)
    else:
        return redirect('admin_login')


def surveyor_list(request, filter):
    if request.user.is_authenticated:
        surveyor = None
        if filter == 'None':
            surveyor = Surveyor.objects.all()[::-1]
        elif filter == 'active':
            surveyor = Surveyor.objects.filter(status=1)[::-1]
        elif filter == 'inactive':
            surveyor = Surveyor.objects.filter(status=0)[::-1]
        paginator = Paginator(surveyor, 25)
        page = request.GET.get('page', )
        all_survey = paginator.get_page(page)
        context = {
            "surveyor": all_survey,
            'isact_surveyorlist': 'active',
        }
        return render(request, 'sadmin_templates/surveyor/surveyor_list.html', context)
    else:
        return redirect('admin_login')


def update_surveyor(request, pid):
    if request.user.is_authenticated:
        s_user = Surveyor.objects.get(id=pid)
        if request.method == "POST":
            fname = request.POST.get('fname', )
            lname = request.POST.get('lname', )
            uname = request.POST.get('uname', )
            password = request.POST.get('password', )
            email = request.POST.get('email', )
            address = request.POST.get('address', )
            country = request.POST.get('country', )
            division = request.POST.get('division', )
            district = request.POST.get('district', )
            sub_district = request.POST.get('sub_district', )
            area = request.POST.get('area', )
            designation = request.POST.get('designation', )
            phone = request.POST.get('phone', )
            s_user.user.first_name = fname
            s_user.user.username = uname
            s_user.user.last_name = lname
            s_user.user.password = make_password(password)
            s_user.user.save()
            s_user.address = address
            s_user.country = country
            s_user.division = division
            s_user.district = district
            s_user.sub_district = sub_district
            s_user.area = area
            s_user.designation = designation
            s_user.phone = phone
            s_user.email = email
            s_user.save()
            messages.success(request, 'Updated successfully!')

        return render(request,'sadmin_templates/surveyor/surveyor_update.html',{'s_user':s_user})
    else:
        return redirect('admin_login')


def view_surveyor(request, id):
    if request.user.is_authenticated:
        single_surveyor = get_object_or_404(Surveyor, id=id)
        context={
            "single_surveyor":single_surveyor,
            'isact_surveyorlist': 'active',

        }
        return render(request, 'sadmin_templates/surveyor/view_surveyor.html', context)
    else:
        return redirect('admin_login')


def surveyor_delete(request, pid):
    if request.user.is_authenticated:
        surveyor = get_object_or_404(Surveyor, id=pid)
        user = User.objects.get(id=surveyor.user.id)
        user.delete()
        messages.warning(request, 'Deleted successfully!')
        return redirect('surveyor_list', filter=None)
    else:
        return redirect('admin_login')


def survey_answer(request, id):
    if request.user.is_authenticated:
        survey_obj = Survey.objects.get(pk=id)
        data_list = []
        questions = survey_obj.question.all()[::-1]
        counter = 0
        for q in questions:
            counter = counter + 1
            data_dict = {
                'questions': q.question_title,
                'ans':[(str(q.ans_type),j.q_ans) for j in Answer.objects.filter(question=q.id).all()]
            }
            data_list.append(data_dict)

        context = {
            "survey": survey_obj,
            'data': data_list,
            'isact_surveylist': 'active',
            "surveyId":id

        }
        return render(request, 'sadmin_templates/survey/survey_answer.html', context)
    else:
        return redirect('admin_login')



def country_add(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            country = request.POST.get('country', )
            user = Country(country_name=country)
            user.save()
            messages.success(request, 'Created successfully')
        get_country = Country.objects.all()[::-1]
        paginator = Paginator(get_country, 10)
        page = request.GET.get('page')
        get_page = paginator.get_page(page)
        context = {
            "get_country": get_page,
            'isact_location': 'active',
        }
        return render(request, 'sadmin_templates/add/add_country.html', context)
    else:
        return redirect('admin_login')


def country_update(request, id):
    if request.user.is_authenticated:
        get_country = get_object_or_404(Country, id=id)
        if request.method == "POST":
            get_country.country_name= request.POST.get('country', )
            update=get_country.save()
            messages.success(request, 'Updated Successfully!')
            return redirect('add_country')

        context = {
            "get_country":get_country,
            'isact_location': 'active',
        }
        return render(request, 'sadmin_templates/update/update_country.html', context)
    else:
        return redirect('admin_login')


def delete_country(request, id):
    if request.user.is_authenticated:
        get_country = get_object_or_404(Country, id=id)
        get_country.delete()
        messages.warning(request, 'Deleted Successfully!')
        return redirect('add_country')
    else:
        return redirect('admin_login')


def division_add(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            division = request.POST.get('division', )
            division_cre = Division(division_name=division)
            division_cre.save()
            messages.success(request, 'Created Successfully!')
        get_division = Division.objects.all()[::-1]
        paginator = Paginator(get_division, 10)
        page = request.GET.get('page')
        get_page = paginator.get_page(page)
        context = {
            "get_division": get_page,
            'isact_location': 'active',
        }
        return render(request, 'sadmin_templates/add/add_division.html', context)
    else:
        return redirect('admin_login')


def division_update(request, id):
    if request.user.is_authenticated:
        get_division = get_object_or_404(Division, id=id)
        if request.method == "POST":
            get_division.division_name= request.POST.get('division', )
            update=get_division.save()
            messages.success(request, 'Updated Successfully!')
            return redirect('add_division')
        context = {
            "get_division":get_division,
            'isact_location': 'active',
        }
        return render(request, 'sadmin_templates/update/update_division.html', context)
    else:
        return redirect('admin_login')


def delete_division(request, id):
    if request.user.is_authenticated:
        get_division = get_object_or_404(Division, id=id)
        get_division.delete()
        messages.warning(request, 'Deleted Successfully!')
        return redirect('add_division')
    else:
        return redirect('admin_login')


def district_add(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            district = request.POST.get('district', )
            district_cre = District(district_name=district)
            district_cre.save()
            messages.success(request, 'Created Successfully!')
        get_district = District.objects.all()[::-1]
        paginator = Paginator(get_district, 25)
        page = request.GET.get('page')
        get_page = paginator.get_page(page)
        context = {
            "get_district": get_page,
            'isact_location': 'active',
        }
        return render(request, 'sadmin_templates/add/add_district.html', context)
    else:
        return redirect('admin_login')


def district_update(request, id):
    if request.user.is_authenticated:
        get_district = get_object_or_404(District, id=id)
        if request.method == "POST":
            get_district.district_name= request.POST.get('district', )
            update=get_district.save()
            messages.success(request, 'Updated Successfully!')
            return redirect('district_add')
        context = {
            "get_district":get_district,
            'isact_location': 'active',
        }
        return render(request, 'sadmin_templates/update/update_district.html', context)
    else:
        return redirect('admin_login')


def delete_district(request, id):
    if request.user.is_authenticated:
        get_district = get_object_or_404(District, id=id)
        get_district.delete()
        messages.warning(request, 'Deleted Successfully!')
        return redirect('district_add')
    else:
        return redirect('admin_login')


def sub_district_add(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            sub_district = request.POST.get('sub_district', )
            sub_district_cre = SubDistrict(subdistrct_name=sub_district)
            sub_district_cre.save()
            messages.success(request, 'Created Successfully!')
        get_sub_district = SubDistrict.objects.all()[::-1]
        paginator = Paginator(get_sub_district, 25)
        page = request.GET.get('page')
        get_page = paginator.get_page(page)
        context = {
            "get_sub_district": get_page,
            'isact_location': 'active',
        }
        return render(request, 'sadmin_templates/add/add_subdistrict.html', context)
    else:
        return redirect('admin_login')


def sub_district_update(request, id):
    if request.user.is_authenticated:
        get_sub_district = get_object_or_404(SubDistrict, id=id)
        if request.method == "POST":
            get_sub_district.subdistrct_name= request.POST.get('sub_district', )
            update=get_sub_district.save()
            messages.success(request, 'Updated Successfully!')
            return redirect('add_sub_district')

        context = {
            "get_sub_district":get_sub_district,
            'isact_location': 'active',
        }
        return render(request, 'sadmin_templates/update/sub_district_update.html', context)
    else:
        return redirect('admin_login')


def delete_sub_district(request, id):
    if request.user.is_authenticated:
        get_sub_district = get_object_or_404(SubDistrict, id=id)
        get_sub_district.delete()
        messages.warning(request, 'Deleted successfully!')
        return redirect('add_sub_district')
    else:
        return redirect('admin_login')


def answer_type_add(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            ans_type = request.POST.get('answer_type', )
            ans_type = ans_type.strip()
            check_ans_type = AnsType.objects.filter(name=ans_type).exists()
            if check_ans_type:
                messages.warning(request, 'Answer Type "{0}" is  Already Exist !!'.format(ans_type))
            if not check_ans_type:
                ans_type_cre = AnsType(name=ans_type)
                ans_type_cre.save()
                messages.success(request, 'Created Successfully!')
        get_ans_type = AnsType.objects.all()[::-1]
        paginator = Paginator(get_ans_type, 10)
        page = request.GET.get('page')
        get_page = paginator.get_page(page)
        context = {
            "get_ans_type": get_page,
            'isact_location': 'active',
        }
        return render(request, 'sadmin_templates/add/add_anstype.html', context)
    else:
        return redirect('admin_login')


def answer_type_update(request, id):
    if request.user.is_authenticated:
        get_ans_type = get_object_or_404(AnsType, id=id)
        if request.method == "POST":
            get_ans_type.name= request.POST.get('answer_type', )
            update=get_ans_type.save()
            messages.success(request, 'Updated Successfully!')
            return redirect('add_answer_type')
        context = {
            "get_ans_type":get_ans_type,
            'isact_location': 'active',
        }
        return render(request, 'sadmin_templates/update/update_ans_type.html', context)
    else:
        return redirect('admin_login')



def delete_answer_type(request, id):
    if request.user.is_authenticated:
        get_ans_type = get_object_or_404(AnsType, id=id)
        get_ans_type.delete()
        messages.warning(request, 'Deleted Successfully!')
        return redirect('add_answer_type')
    else:
        return redirect('admin_login')

