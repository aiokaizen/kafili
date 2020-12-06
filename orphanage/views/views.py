from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout as django_logout

from orphanage.decorators import valid_session
from orphanage.forms import ConnectionForm, RegistrationForm
from orphanage.models import Child, Year, Grade, Subject, Guardian


def connexion(request):
    user = request.user if request.user.is_authenticated else None
    if request.method == 'POST':
        form = ConnectionForm(request.POST)
        if not user:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
        if user and user.is_active:
            login(request, user)
            url = request.GET.get('next') if 'next' in request.GET else reverse('orphanage:home')
            return redirect(url)
        else:
            form.add_error('username', 'إسم المستخدم أو كلمة المرور خاطئة.')
    else:
        form = ConnectionForm()

    return render(request, 'orphanage/authentication/login.html', {
        'form': form,
    })


def request_registration(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'orphanage/authentication/request_registration_finish.html')
    else:
        form = RegistrationForm()

    return render(request, 'orphanage/authentication/request_registration.html', {
        'form': form,
    })


@login_required
def year_switch(request, year):
    year = get_object_or_404(Year, year=year)
    print('year:', year)
    request.session['year'] = year.year
    messages.success(request, f"أنت الآن متصل ضمن فضاء السنة الدراسية {year}")
    if 'HTTP_REFERER' in request.META:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(reverse('orphanage:home'))


@login_required
def logout(request):
    django_logout(request)
    return redirect(reverse('orphanage:login'))


@login_required
@valid_session
def home(request):
    
    children_count = Child.objects.count()
    grades_count = Grade.objects.count()
    subjects_count = Subject.objects.count()
    guardians_count = Guardian.objects.count()

    context = {
        'page_title': 'Home',
        'page_title_ar': 'الصفحة الرئيسية',
        'children_count': children_count,
        'grades_count': grades_count,
        'subjects_count': subjects_count,
        'guardians_count': guardians_count,
    }

    return render(request, 'orphanage/home.html', context)


@login_required
@valid_session
def profile(request):

    context = {
        'page_title': 'Profile'
    }

    return render(request, 'orphanage/profile.html', context)
