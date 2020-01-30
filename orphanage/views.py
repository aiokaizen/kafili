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


@login_required
def profile(request):

    return render(request, 'orphanage/profile.html')


@login_required
def children_list(request):
    children = Child.list()

    number_per_page = 20
    next_page = None
    previous_page = None

    paginator = Paginator(children, number_per_page)
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
    }

    return render(request, 'orphanage/children_list.html', context)


@login_required
def child_details(request, id):
    child = Child.objects.get(pk=id)

    context = {
        'child': child,
    }

    return render(request, 'orphanage/child_details.html', context)


@login_required
def child_insert(request):
    
    form = ChildForm()

    context = {
        'form': form
    }

    return render(request, 'orphanage/child_update.html', context)


@login_required
def child_update(request, id):

    try:
        child = Child.objects.get(id=id)
    except ObjectDoesNotExist:
        return Http404()

    if request.method == 'POST':
        form = ChildForm(data=request.POST, files=request.FILES, instance=child)
        if form.is_valid():
            form.instance.birthday = form.cleaned_data['birthday']
            form.instance.save()
            return redirect(reverse('orphanage:child_details', args=[child.id]))
    else:
        form = ChildForm(instance=child, initial={'birthday': child.birthday})

    context = {
        'form': form,
    }

    return render(request, 'orphanage/child_update.html', context)
