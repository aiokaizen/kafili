from django.shortcuts import render_to_response


def handler_404(request, exception):
    template_name = 'orphanage/errors/404.html'
    response = render_to_response(template_name)
    response.status_code = 404
    return response


def handler_500(request):
    template_name = 'orphanage/errors/500.html'
    response = render_to_response(template_name)
    response.status_code = 500
    return response


def handler_403(request, exception):  # permission denied
    template_name = 'orphanage/errors/403.html'
    response = render_to_response(template_name)
    response.status_code = 403
    return response

