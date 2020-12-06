from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from orphanage import settings as orphanage_settings
from orphanage.decorators import valid_session
from orphanage.forms import GradeForm, SubjectForm
from orphanage.models import Grade, Year, Student, Subject


@login_required
@valid_session
def grades(request):

    year = Year.objects.get(year=request.session['year'])

    grades_qset = Grade.list(year=year, **request.GET)

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

    if request.method == 'POST':
        if request.POST.get('action') == 'delete_multiple':
            grades = Grade.objects.filter(pk__in=request.POST.getlist('objects_ids', ''))
            res, message = Grade.delete_grades(grades)
            if res:
                messages.success(request, message)
            else:
                messages.error(request, message)
            return redirect(reverse('orphanage:grades'))


    context = {
        'items': queryset,
        'table_size': table_size,
        'page': page,
        'number_of_pages': paginator.num_pages,
        'range': paginator.page_range,
        'next_page': next_page,
        'previous_page': previous_page,
        'page_title': 'Grades',
        'page_title_ar': 'لائحة المستويات'
    }

    return render(request, 'orphanage/grade/grades_list.html', context)


@login_required
@valid_session
def grade_insert(request):

    year = Year.objects.get(year=request.session['year'])
    
    if request.method == 'POST':
        form = GradeForm(data=request.POST)
        if form.is_valid():
            success, message = form.instance.create_grade(year)
            if success:
                messages.success(request, message)
                return redirect(reverse('orphanage:grade_details', args=[form.instance.id]))
            else:
                messages.error(request, message)
    else:
        form = GradeForm()

    context = {
        'form': form,
        'page_title': 'Grade insert',
        'page_title_ar': 'إضافة مستوى'
    }

    return render(request, 'orphanage/grade/grade_update.html', context)


@login_required
@valid_session
def grade_details(request, grade_id):
    
    grade = get_object_or_404(Grade, id=grade_id)
    subjects = Subject.list(grade=grade)
    students_count = Student.list(grade=grade).count()

    if request.method == 'POST':
        if request.POST['action'] == 'delete':
            success, message = grade.delete_grade()
            if success:
                messages.success(request, message)
                return redirect(reverse('orphanage:grades'))
            else:
                messages.error(request, message)
        elif request.POST['action'] == 'create_subject':
            subject_form = SubjectForm(data=request.POST, instance=Subject())
            if subject_form.is_valid():
                success, message = subject_form.instance.create_subject(grade)
                if success:
                    messages.success(request, message)
                    return redirect(request.get_full_path())
                else:
                    messages.error(request, message)
        elif request.POST['action'] == 'delete_subject':
            subject_id = request.POST.get('id')
            subject = get_object_or_404(Subject, pk=subject_id)
            success, message = subject.delete_subject()
            if success:
                messages.success(request, message)
                return redirect(request.get_full_path())
            else:
                messages.error(request, message)

    else:
        subject_form = SubjectForm(instance=Subject())

    context = {
        'grade': grade,
        'subjects': subjects,
        'subject_form': subject_form,
        'students_count': students_count,
        'page_title': 'Grade details',
        'page_title_ar': f"المستوى {grade}",
    }

    return render(request, 'orphanage/grade/grade_details.html', context)


@login_required
@valid_session
def grade_update(request, grade_id):

    grade = get_object_or_404(Grade, id=grade_id)

    if request.method == 'POST':
        form = GradeForm(data=request.POST, instance=grade)
        if form.is_valid():
            success, message = form.instance.update_grade()
            if success:
                messages.success(request, message)
                return redirect(reverse('orphanage:grade_details', args=[grade.id]))
            else:
                messages.error(request, message)
    else:
        form = GradeForm(instance=grade)

    context = {
        'form': form,
        'page_title': 'Grade update'
    }

    return render(request, 'orphanage/grade/grade_update.html', context)
