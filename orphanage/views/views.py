from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout as django_logout

from orphanage.forms import ConnectionForm, ChildForm
from orphanage.models import Child
from orphanage.views.printing import print_cards


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
        form = ConnectionForm()

    return render(request, 'orphanage/login.html', {
        'form': form,
    })


def logout(request):
    django_logout(request)
    return redirect(reverse('orphanage:login'))


def home(request):
    context = {
        'page_title': 'Home',
    }

    return render(request, 'orphanage/home.html', context)


@login_required
def profile(request):

    context = {
        'page_title': 'Profile'
    }

    return render(request, 'orphanage/profile.html', context)


@login_required
def children(request):
    qset = Child.list(**request.GET)

    if request.method == 'POST':
        if request.POST['action'] == 'print':
            return print_cards(request)

    number_per_page = 20
    next_page = None
    previous_page = None

    paginator = Paginator(qset, number_per_page)
    if request.GET.get('page'):
        page = request.GET.get('page')
    else:
        page = 1
    try:
        orphans_page = paginator.page(page)
    except PageNotAnInteger:
        orphans_page = paginator.page(1)
    except EmptyPage:
        orphans_page = paginator.page(paginator.num_pages)

    if orphans_page.has_next():
        next_page = orphans_page.next_page_number()
    if orphans_page.has_previous():
        previous_page = orphans_page.previous_page_number()

    context = {
        'items': orphans_page,
        'number_per_page': number_per_page,
        'page': page,
        'number_of_pages': paginator.num_pages,
        'range': paginator.page_range,
        'next_page': next_page,
        'previous_page': previous_page,
        'page_title': 'Children'
    }

    return render(request, 'orphanage/children_list.html', context)


@login_required
def child_details(request, child_id):
    child = Child.objects.get(pk=child_id)

    context = {
        'child': child,
        'page_title': 'Child details'
    }

    # from weasyprint import HTML
    # HTML(request.get_full_path()).write_pdf('/tmp/weasyprint-website.pdf')

    return render(request, 'orphanage/child_details.html', context)


@login_required
def child_insert(request):
    
    form = ChildForm()

    context = {
        'form': form,
        'page_title': 'Child insert'
    }

    return render(request, 'orphanage/child_update.html', context)


@login_required
def child_update(request, child_id):

    try:
        child = Child.objects.get(id=child_id)
    except ObjectDoesNotExist:
        return Http404()

    if request.method == 'POST':
        form = ChildForm(data=request.POST, files=request.FILES, instance=child)
        if form.is_valid():
            form.instance.birthday = form.cleaned_data['birthday']
            form.instance.save()
            child_title = 'الطفل' if child.sex == 'm' else 'الطفلة'
            messages.success(request, 'تمت عملية تحديث بيانات ' + child_title + ' بنجاح.')
            return redirect(reverse('orphanage:child_details', args=[child.id]))
        messages.error(request, 'المرجو مراجعة بيانات التلميذ(ة)')
    else:
        form = ChildForm(instance=child, initial={'birthday': child.birthday})

    context = {
        'form': form,
        'page_title': 'Child update'
    }

    return render(request, 'orphanage/child_update.html', context)
