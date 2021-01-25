from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from orphanage import settings as orphanage_settings
from orphanage.decorators import valid_session
from orphanage.forms import ChildForm, ChildFilterForm
from orphanage.models import Child


@login_required
@valid_session
def children(request):

    qset = Child.list(**request.GET)

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
        if request.POST.get('action', '') == 'delete_multiple':
            children = Child.objects.filter(pk__in=request.POST.getlist('objects_ids', ''))
            res, message = Child.delete_children(children)
            if res:
                messages.success(request, message)
            else:
                messages.error(request, message)
            return redirect(reverse('orphanage:children'))
        elif request.POST.get('action', '') == 'import_pictures':
            res, message, err_msg = Child.import_photos()
            messages.success(request, message)
            if err_msg:
                messages.warning(request, err_msg)
            return redirect(reverse('orphanage:children'))

    context = {
        'items': orphans_page,
        'table_size': table_size,
        'page': page,
        'filter_form': ChildFilterForm(initial=initial_dict),
        'number_of_pages': paginator.num_pages,
        'range': paginator.page_range,
        'next_page': next_page,
        'previous_page': previous_page,
        'page_title': 'Children',
        'page_title_ar': 'لائحة الأطفال'
    }

    return render(request, 'orphanage/child/children_list.html', context)


@login_required
@valid_session
def child_insert(request):
    
    if request.method == 'POST':
        form = ChildForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.instance.birthday = form.cleaned_data['birthday']
            form.instance.save()
            child_title = 'الطفل' if form.instance.sex == 'm' else 'الطفلة'
            messages.success(request, 'تمت إضافة ' + child_title + ' بنجاح.')
            return redirect(reverse('orphanage:child_details', args=[form.instance.id]))
        messages.error(request, 'المرجو مراجعة بيانات الطفل(ة)')
    else:
        form = ChildForm()

    context = {
        'form': form,
        'page_title': 'Child insert',
        'page_title_ar': f'إضافة تلميذ(ة)'
    }

    return render(request, 'orphanage/child/child_update.html', context)


@login_required
@valid_session
def child_details(request, child_id):
    
    child = get_object_or_404(Child, id=child_id)
    child_title = 'الطفل' if child.sex == 'm' else 'الطفلة'

    if request.method == 'POST':
        if request.POST['action'] == 'delete':
            child.delete()
            return redirect(reverse('orphanage:children'))

    context = {
        'child': child,
        'page_title': 'Child details',
        'page_title_ar': f'بيانات {child_title} {child}'
    }

    return render(request, 'orphanage/child/child_details.html', context)


@login_required
@valid_session
def child_update(request, child_id):

    child = get_object_or_404(Child, id=child_id)

    if request.method == 'POST':
        form = ChildForm(data=request.POST, files=request.FILES, instance=child)
        if form.is_valid():
            form.instance.birthday = form.cleaned_data['birthday']
            form.instance.save()
            child_title = 'الطفل' if child.child.sex == 'm' else 'الطفلة'
            messages.success(request, 'تمت عملية تحديث بيانات ' + child_title + ' بنجاح.')
            return redirect(reverse('orphanage:child_details', args=[child.id]))
        messages.error(request, f'المرجو مراجعة بيانات الطفل(ة) {form.errors}')
    else:
        form = ChildForm(instance=child, initial={'birthday': child.birthday})

    context = {
        'form': form,
        'page_title': 'Child update',
        'page_title_ar': f'تحديث بيانات الأطفال {child}'
    }

    return render(request, 'orphanage/child/child_update.html', context)


@login_required
@valid_session
def child_marks(request, child_id):
    
    child = get_object_or_404(Child, id=child_id)

    if request.method == 'POST':
        if request.POST['action'] == 'delete':
            child.delete()
            return redirect(reverse('orphanage:children'))

    context = {
        'child': child,
        'page_title': 'Child marks',
        'page_title_ar': f'علامات الأطفال {child}'
    }

    return render(request, 'orphanage/child/child_marks.html', context)
