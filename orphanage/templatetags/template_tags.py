from django import template

from kafili.local_settings import BREADCRUMBS_DEPTH_LEVEL
from orphanage.breadcrumbs import get_page
from orphanage.utils import get_page_parents as get_parents

register = template.Library()


def in_range_3(current, index):
    return in_range(current, index, 3)


def in_range(current, index, range):
    max = current + range
    min = current - range

    if index > max or index < min:
        return False
    return True


def get_breadcrumbs(page_title, path):
    page = get_page(page_title)
    depth = BREADCRUMBS_DEPTH_LEVEL
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


register.filter('in_range_3', in_range_3)
register.filter('get_breadcrumbs', get_breadcrumbs)
