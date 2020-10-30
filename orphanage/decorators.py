from datetime import datetime
from functools import wraps
from django.shortcuts import redirect, reverse
from django.core.exceptions import PermissionDenied

from orphanage.models import Year

def valid_session(function):
    def _dec(view_func):
        def _view(request, *args, **kwargs):
            if 'year' not in request.session:
                year = Year.objects.first()
                if year:
                    request.session['year'] = year.year
                else:
                    # First connection, No Year objects are found
                    year = datetime.now().year if datetime.now().month > 8 else datetime.now().year - 1
                    Year.objects.create(year=year)
                    request.session['year'] = year
            return view_func(request, *args, **kwargs)
        return _view
    
    if function is None:
        return _dec
    else:
        return _dec(function)
