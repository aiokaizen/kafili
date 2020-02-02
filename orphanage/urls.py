from django.conf.urls import url

from orphanage.views import *

app_name = 'orphanage'

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^login/$', connexion, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^children/$', children, name='children'),
    url(r'^children/print_cards$', print_cards, name='print_cards'),
    url(r'^children/(?P<child_id>[0-9]+)/$', child_details, name='child_details'),
    url(r'^children/(?P<child_id>[0-9]+)/print_card$', print_cards, name='print_card'),
    url(r'^children/(?P<child_id>[0-9]+)/update/$', child_update, name='child_update'),
    url(r'^children/insert/$', child_insert, name='child_insert'),
    # url(r'^print_test/$', render_pdf_view, name='test_print'),
    # url(r'^print_test/$', PDFTemplateView.as_view(
    #     template_name='orphanage/children_list.html', filename='my_pdf.pdf'), name='pdf')
]
