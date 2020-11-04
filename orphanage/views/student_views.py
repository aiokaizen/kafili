from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from orphanage import settings as orphanage_settings
from orphanage.decorators import valid_session
from orphanage.forms import StudentForm, StudentFilterForm
from orphanage.models import Student


@login_required
@valid_session
def students(request):

    qset = Student.list(**request.GET)

    table_size = orphanage_settings.TABLE_SIZE
    if 'tablesize' in request.GET:
        try:
            tmp_table_size = int(request.GET['tablesize'])
            if tmp_table_size > 0:
                table_size = tmp_table_size
        except ValueError:
            pass
    next_page = None
    previous_page = None

    paginator = Paginator(qset, table_size)
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

    initial_dict = {}
    for key in request.GET.keys():
        if request.GET[key]:
            initial_dict[key] = request.GET[key]

    # POST METHOD
    if request.method == 'POST':
        if request.POST.get('action', '') == 'delete':
            students = Student.objects.filter(pk__in=request.POST.getlist('students_ids', ''))
            res, message = Student.delete_students(students)
            if res:
                messages.success(request, message)
            else:
                messages.error(request, message)
            return redirect(reverse('orphanage:students'))
        elif request.POST.get('action', '') == 'import_pictures':
            res, message, err_msg = Student.import_photos()
            messages.success(request, message)
            if err_msg:
                messages.warning(request, err_msg)
            return redirect(reverse('orphanage:students'))

    context = {
        'items': orphans_page,
        'table_size': table_size,
        'page': page,
        'filter_form': StudentFilterForm(initial=initial_dict),
        'number_of_pages': paginator.num_pages,
        'range': paginator.page_range,
        'next_page': next_page,
        'previous_page': previous_page,
        'page_title': 'Students',
        'page_title_ar': 'لائحة التلاميذ'
    }

    return render(request, 'orphanage/student/students_list.html', context)


@login_required
@valid_session
def student_insert(request):
    
    if request.method == 'POST':
        form = StudentForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.instance.birthday = form.cleaned_data['birthday']
            form.instance.save()
            student_title = 'الطفل' if form.instance.sex == 'm' else 'الطفلة'
            messages.success(request, 'تمت إضافة ' + student_title + ' بنجاح.')
            return redirect(reverse('orphanage:student_details', args=[form.instance.id]))
        messages.error(request, 'المرجو مراجعة بيانات التلميذ(ة)')
    else:
        form = StudentForm()

    context = {
        'form': form,
        'page_title': 'Student insert'
    }

    return render(request, 'orphanage/student/student_update.html', context)


@login_required
@valid_session
def student_details(request, student_id):
    
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        if request.POST['action'] == 'delete':
            student.delete()
            return redirect(reverse('orphanage:students'))

    context = {
        'student': student,
        'page_title': 'Student details'
    }

    return render(request, 'orphanage/student/student_details.html', context)


@login_required
@valid_session
def student_update(request, student_id):

    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        form = StudentForm(data=request.POST, files=request.FILES, instance=student)
        if form.is_valid():
            form.instance.birthday = form.cleaned_data['birthday']
            form.instance.save()
            student_title = 'الطفل' if student.sex == 'm' else 'الطفلة'
            messages.success(request, 'تمت عملية تحديث بيانات ' + student_title + ' بنجاح.')
            return redirect(reverse('orphanage:student_details', args=[student.id]))
        messages.error(request, 'المرجو مراجعة بيانات التلميذ(ة)')
    else:
        form = StudentForm(instance=student, initial={'birthday': student.birthday})

    context = {
        'form': form,
        'page_title': 'Student update'
    }

    return render(request, 'orphanage/student/student_update.html', context)


@login_required
@valid_session
def student_marks(request, student_id):
    
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        if request.POST['action'] == 'delete':
            student.delete()
            return redirect(reverse('orphanage:students'))

    context = {
        'student': student,
        'page_title': 'Student details'
    }

    return render(request, 'orphanage/student/student_marks.html', context)
