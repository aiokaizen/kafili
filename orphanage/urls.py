from django.conf.urls import url
from wkhtmltopdf.views import PDFTemplateView

from orphanage.views import *

app_name = 'orphanage'

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^login/$', connexion, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^profile/$', profile, name='profile'),

    # Children
    url(r'^children/$', children, name='children'),
    url(r'^children/insert/$', child_insert, name='child_insert'),
    url(r'^children/print_cards/$', ChildCardPDF.as_view(), name='print_cards'),
    url(r'^children/(?P<child_id>[0-9]+)/$', child_details, name='child_details'),
    url(r'^children/(?P<child_id>[0-9]+)/print_card/$', ChildCardPDF.as_view(), name='print_card'),
    url(r'^children/(?P<child_id>[0-9]+)/update/$', child_update, name='child_update'),
    url(r'^children/(?P<child_id>[0-9]+)/marks/$', child_marks, name='child_marks'),
    
    # Guardians
    # url(r'^guardians/$', guardians, name='guardians'),
    # url(r'^guardians/(?P<guardian_id>[0-9]+)/$', guardian_details, name='guardian_details'),
    # url(r'^guardians/(?P<guardian_id>[0-9]+)/update/$', guardian_update, name='guardian_update'),
    # url(r'^guardians/insert/$', guardian_insert, name='guardian_insert'),
    
    # Years
    url(r'^year/$', year_details, name='year_details'),
    url(r'^year/insert/$', year_insert, name='year_insert'),
    url(r'^year/switch/(?P<year>[0-9]{4})/$', year_switch, name='year_switch'),
    
    # Grades
    url(r'^grades/$', grades, name='grades'),
    url(r'^grades/(?P<grade_id>[0-9]+)/$', grade_details, name='grade_details'),
    url(r'^grades/(?P<grade_id>[0-9]+)/update/$', grade_update, name='grade_update'),
    url(r'^grades/insert/$', grade_insert, name='grade_insert'),
    
    # Subjects
    # url(r'^grades/(?P<grade_id>[0-9]+)/subjects/$', subjects, name='subjects'),
    # url(r'^grades/(?P<grade_id>[0-9]+)/subjects/(?P<subject_id>[0-9]+)/$', subject_details, name='subject_details'),
    # url(r'^grades/(?P<grade_id>[0-9]+)/subjects/(?P<subject_id>[0-9]+)/update/$', subject_update, name='subject_update'),
    # url(r'^grades/(?P<grade_id>[0-9]+)/subjects/insert/$', subject_insert, name='subject_insert'),
]
