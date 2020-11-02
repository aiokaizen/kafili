from django.contrib import messages
from django.http import Http404
from django.template.response import TemplateResponse

from wkhtmltopdf.views import PDFTemplateView, PDFTemplateResponse

from orphanage.models import Student

# import os
# from django.conf import settings
# from django.http import HttpResponse
# from django.template import Context
# from django.template.loader import get_template
# from xhtml2pdf import pisa
#
#
# def link_callback(uri, rel):
#     """
#     Convert HTML URIs to absolute system paths so xhtml2pdf can access those
#     resources
#     """
#     # use short variable names
#     sUrl = settings.STATIC_URL      # Typically /static/
#     sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
#     mUrl = settings.MEDIA_URL       # Typically /static/media/
#     mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/
#
#     # convert URIs to absolute system paths
#     if uri.startswith(mUrl):
#         path = os.path.join(mRoot, uri.replace(mUrl, ""))
#     elif uri.startswith(sUrl):
#         path = os.path.join(sRoot, uri.replace(sUrl, ""))
#     else:
#         return uri  # handle absolute uri (ie: http://some.tld/foo.png)
#
#     # make sure that file exists
#     if not os.path.isfile(path):
#             raise Exception(
#                 'media URI must start with %s or %s' % (sUrl, mUrl)
#             )
#     return path
#
#
# def render_pdf_view(request):
#     template_path = 'user_printer.html'
#     context = {'myvar': 'this is your template context'}
#     # Create a Django response object, and specify content_type as pdf
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="report.pdf"'
#     # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(Context(context))
#
#     # create a pdf
#     pisaStatus = pisa.CreatePDF(
#        html, dest=response, link_callback=link_callback)
#     # if error then show some funy view
#     if pisaStatus.err:
#        return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response
from orphanage.utils import get_scholar_year


class StudentCardPDF(PDFTemplateView):

    cmd_options = {
        'page-width': '140',
        'page-height': '80',
        'orientation': 'portrait',
        'margin-top': 0,
        'margin-bottom': 0,
        'margin-left': 0,
        'margin-right': 0,
    }

    filename = None

    template_name = 'orphanage/pdf/student_card.html'

    context = {}

    def get(self, request, *args, **kwargs):

        if 'student_id' in kwargs:
            students = Student.objects.filter(pk=kwargs['student_id'])
            if not students:
                raise Http404()
            student_title = 'التلميذ' if students[0].sex == 'm' else 'التلميذة'
            messages.success(request, 'لقد تمت طباعة بطاقة ' + student_title + ' بنجاح.')
        else:
            if 'students_ids' in kwargs:
                students = Student.objects.filter(id__in=kwargs['students_ids'])
            else:
                students = Student.objects.all()
            messages.success(request, 'تمت طباعة بطاقات الأطفال بنجاح.')

        self.context['students'] = students
        self.context['scholar_year'] = get_scholar_year(switch_month=6)

        if request.GET.get('as', '') == 'html':
            return TemplateResponse(
                request=request, template=self.template_name, context=self.context,
            )

        return PDFTemplateResponse(
            request=request, template=self.template_name, filename=self.filename, context=self.context,
            show_content_in_browser=False, cmd_options=self.cmd_options,
        )
