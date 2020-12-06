from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from orphanage import settings as orphanage_settings
from orphanage.decorators import valid_session
from orphanage.forms import SubjectForm
from orphanage.models import Subject


@login_required
@valid_session
def subjects(request):

    qset = Subject.list(**request.GET)

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
            subjects = Subject.objects.filter(pk__in=request.POST.getlist('subjects_ids', ''))
            res, message = Subject.delete_subjects(subjects)
            if res:
                messages.success(request, message)
            else:
                messages.error(request, message)
            return redirect(reverse('orphanage:subjects'))
        elif request.POST.get('action', '') == 'import_pictures':
            res, message, err_msg = Subject.import_photos()
            messages.success(request, message)
            if err_msg:
                messages.warning(request, err_msg)
            return redirect(reverse('orphanage:subjects'))

    context = {
        'items': orphans_page,
        'table_size': table_size,
        'page': page,
        # 'filter_form': SubjectFilterForm(initial=initial_dict),
        'number_of_pages': paginator.num_pages,
        'range': paginator.page_range,
        'next_page': next_page,
        'previous_page': previous_page,
        'page_title': 'Subjects',
        'page_title_ar': 'لائحة التلاميذ'
    }

    return render(request, 'orphanage/subject/subjects_list.html', context)


@login_required
@valid_session
def subject_insert(request):
    
    if request.method == 'POST':
        form = SubjectForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.instance.birthday = form.cleaned_data['birthday']
            form.instance.save()
            subject_title = 'الطفل' if form.instance.sex == 'm' else 'الطفلة'
            messages.success(request, 'تمت إضافة ' + subject_title + ' بنجاح.')
            return redirect(reverse('orphanage:subject_details', args=[form.instance.id]))
        messages.error(request, 'المرجو مراجعة بيانات التلميذ(ة)')
    else:
        form = SubjectForm()

    context = {
        'form': form,
        'page_title': 'Subject insert',
        'page_title_ar': f'إضافة تلميذ(ة)'
    }

    return render(request, 'orphanage/subject/subject_update.html', context)


@login_required
@valid_session
def subject_details(request, subject_id):
    
    subject = get_object_or_404(Subject, id=subject_id)
    subject_title = 'التلميذ' if subject.sex == 'm' else 'التلميذة'

    if request.method == 'POST':
        if request.POST['action'] == 'delete':
            subject.delete()
            return redirect(reverse('orphanage:subjects'))

    context = {
        'subject': subject,
        'page_title': 'Subject details',
        'page_title_ar': f'بيانات {subject_title} {subject}'
    }

    return render(request, 'orphanage/subject/subject_details.html', context)


@login_required
@valid_session
def subject_update(request, subject_id):

    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == 'POST':
        form = SubjectForm(data=request.POST, files=request.FILES, instance=subject)
        if form.is_valid():
            form.instance.birthday = form.cleaned_data['birthday']
            form.instance.save()
            subject_title = 'الطفل' if subject.sex == 'm' else 'الطفلة'
            messages.success(request, 'تمت عملية تحديث بيانات ' + subject_title + ' بنجاح.')
            return redirect(reverse('orphanage:subject_details', args=[subject.id]))
        messages.error(request, f'المرجو مراجعة بيانات التلميذ(ة) {form.errors}')
    else:
        form = SubjectForm(instance=subject, initial={'birthday': subject.birthday})

    context = {
        'form': form,
        'page_title': 'Subject update',
        'page_title_ar': f'تحديث بيانات التلاميذ {subject}'
    }

    return render(request, 'orphanage/subject/subject_update.html', context)


@login_required
@valid_session
def subject_marks(request, subject_id):
    
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == 'POST':
        if request.POST['action'] == 'delete':
            subject.delete()
            return redirect(reverse('orphanage:subjects'))

    context = {
        'subject': subject,
        'page_title': 'Subject marks',
        'page_title_ar': f'علامات التلاميذ {subject}'
    }

    return render(request, 'orphanage/subject/subject_marks.html', context)
