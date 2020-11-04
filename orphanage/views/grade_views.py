from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from orphanage import settings as orphanage_settings
from orphanage.decorators import valid_session
from orphanage.forms import GradeForm
from orphanage.models import Grade


@login_required
@valid_session
def grades(request):

    grades_qset = Grade.list(**request.GET)

    table_size = orphanage_settings.TABLE_SIZE
    next_page = None
    previous_page = None

    paginator = Paginator(grades_qset, table_size)
    if request.GET.get('page'):
        page = request.GET.get('page')
    else:
        page = 1
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    if queryset.has_next():
        next_page = queryset.next_page_number()
    if queryset.has_previous():
        previous_page = queryset.previous_page_number()

    context = {
        'items': queryset,
        'table_size': table_size,
        'page': page,
        'number_of_pages': paginator.num_pages,
        'range': paginator.page_range,
        'next_page': next_page,
        'previous_page': previous_page,
        'page_title': 'grades'
    }

    return render(request, 'orphanage/grade/grades_list.html', context)


@login_required
@valid_session
def grade_insert(request):
    
    if request.method == 'POST':
        form = GradeForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تمت إضافة المستوى الدراسي بنجاح.')
            return redirect(reverse('orphanage:grade_details', args=[form.instance.id]))
        messages.error(request, 'المرجو مراجعة بيانات المستوى الدراسي')
    else:
        form = GradeForm()

    context = {
        'form': form,
        'page_title': 'Grade insert'
    }

    return render(request, 'orphanage/grade/grade_update.html', context)


@login_required
@valid_session
def grade_details(request, grade_id):
    
    grade = get_object_or_404(Grade, id=grade_id)

    if request.method == 'POST':
        if request.POST['action'] == 'delete':
            grade.delete()
            return redirect(reverse('orphanage:grades'))

    context = {
        'grade': grade,
        'page_title': 'Grade details'
    }

    return render(request, 'orphanage/grade/grade_details.html', context)


@login_required
@valid_session
def grade_update(request, grade_id):

    grade = get_object_or_404(Grade, id=grade_id)

    if request.method == 'POST':
        form = GradeForm(data=request.POST, instance=grade)
        if form.is_valid():
            form.save()
            messages.success(request, 'تمت عملية تحديث بيانات المستوى الدراسي بنجاح.')
            return redirect(reverse('orphanage:grade_details', args=[grade.id]))
        messages.error(request, 'المرجو مراجعة بيانات المستوى الدراسي')
    else:
        form = GradeForm(instance=grade)

    context = {
        'form': form,
        'page_title': 'Grade update'
    }

    return render(request, 'orphanage/grade/grade_update.html', context)
