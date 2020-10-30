from orphanage.models import Year

def main_context(request):

    year = None
    years = []
    if 'year' in request.session:
        year = Year.objects.get(year=request.session['year'])
        years = Year.objects.exclude(pk=year.id)
    context = {
        'current_year': year,
        'years': years
    }

    return context
