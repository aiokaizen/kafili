from orphanage.models import Year, Student, Grade, Subject, Guardian


def main_context(request):

    year = None
    years = []
    if 'year' in request.session:
        year = Year.objects.get(year=request.session['year'])
        years = Year.objects.exclude(pk=year.id)
    students_count = Student.objects.count()
    grades_count = Grade.objects.count()
    subjects_count = Subject.objects.count()
    guardians_count = Guardian.objects.count()
    context = {
        'current_year': year,
        'years': years,
        'students_count': students_count,
        'grades_count': grades_count,
        'subjects_count': subjects_count,
        'guardians_count': guardians_count,
    }

    return context
