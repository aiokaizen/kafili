import pdfkit
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from wkhtmltopdf.views import PDFTemplateView, PDFTemplateResponse

from orphanage.models import Child

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


def print_cards(request, child_id=''):

    if child_id != '':
        try:
            child = Child.objects.get(pk=child_id)
            print('printing card for:', child)
            child_title = 'الطفل' if child.sex == 'm' else 'الطفلة'





            pdf = pdfkit.from_url(request.get_host() + '', False)
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="ourcodeworld.pdf"'

            return response





            messages.success(request, 'لقد تمت طباعة بطاقة ' + child_title + ' بنجاح.')
            return redirect(reverse('orphanage:child_details', kwargs={'child_id': child_id}))
        except ObjectDoesNotExist:
            raise Http404()
    else:
        if 'children' in request.POST:
            children_ids = request.POST.getlist('children')
            children = Child.list(ids=children_ids)
            print('printing cards for selected children')
            messages.success(request, 'تمت طباعة بطاقات الأطفال بنجاح.')
        else:
            children = Child.objects.all()
            print('printing cards for all children')
            # html = HTML('http://weasyprint.org/').write_pdf('/tmp/weasyprint-website.pdf')
            messages.success(request, 'تمت طباعة بطاقات الأطفال بنجاح.')

    return redirect(reverse('orphanage:children'))


class ChildCardPDF(PDFTemplateView):

    cmd_options = {
        # 'page-size': 'A4',
        'page-width': '140',
        'page-height': '80',
        'orientation': 'portrait',  # ''landscape',
        'margin-top': 0,
        'margin-bottom': 0,
        'margin-left': 0,
        'margin-right': 0,
    }

    # filename = 'child_card.pdf'
    filename = None

    template_name = 'orphanage/pdf/child_card.html'
    header_template = 'orphanage/pdf/header.html'
    footer_template = 'orphanage/pdf/footer.html'

    def get(self, request, *args, **kwargs):

        context = {}

        if 'child_id' in kwargs:
            child = Child.objects.get(pk=kwargs['child_id'])
            context['child'] = child
        else:
            children = Child.objects.all()[:10]
            context['children'] = children

        response = PDFTemplateResponse(
            request=request, template=self.template_name, filename=self.filename, context=context,
            show_content_in_browser=False, cmd_options=self.cmd_options,
        )
        return response
