from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from orphanage import settings as orphanage_settings
from orphanage.decorators import valid_session
from orphanage.forms import YearForm
from orphanage.models import Year


@login_required
@valid_session
def year_insert(request):
    
    if request.method == 'POST':
        form = YearForm(data=request.POST)
        if form.is_valid():
            form.instance.save()
            messages.success(request, 'تمت إضافة السنة بنجاح.')
            return redirect(reverse('orphanage:year_details'))
        messages.error(request, 'المرجو مراجعة بيانات التلميذ(ة)')
    else:
        form = YearForm()

    context = {
        'form': form,
        'page_title': 'Year insert'
    }

    return render(request, 'orphanage/year/year_create.html', context)


@login_required
@valid_session
def year_details(request):
    
    year = get_object_or_404(Year, year=request.session.get('year'))

    context = {
        'year': year,
        'page_title': 'Year'
    }

    return render(request, 'orphanage/year/year_details.html', context)
