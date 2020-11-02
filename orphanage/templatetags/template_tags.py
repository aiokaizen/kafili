from django import template

from orphanage import settings as orphanage_settings
from orphanage.breadcrumbs import get_page
from orphanage.utils import get_page_parents as get_parents

register = template.Library()


def in_range(current, index, range):
    max = current + range
    min = current - range

    if index > max or index < min:
        return False
    return True


@register.filter()
def in_range_2(current, index):
    return in_range(current, index, 2)


@register.filter()
def get_breadcrumbs(page_title, path):
    page = get_page(page_title)
    depth = orphanage_settings.BREADCRUMBS_DEPTH_LEVEL
    if page:
        parents = get_parents(page)
        parent_url = ''
        index = 0
        path_fragments = path.split('/')[1:-2]
        for parent in parents:
            parent_url += '/' + path_fragments[index]
            parent.url = parent_url
            index += 1
        if len(parents) > depth:
            return parents[-depth:], page.label
        return parents, page.label

    return [], page_title
