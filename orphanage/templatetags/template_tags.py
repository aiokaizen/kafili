from django import template

register = template.Library()


def in_range_3(current, index):
    return in_range(current, index, 3)


def in_range(current, index, range):
    max = current + range
    min = current - range

    if index > max or index < min:
        return False
    return True


register.filter('in_range_3', in_range_3)
