from django.conf import settings


TABLE_MAX_ITEMS = getattr(settings, 'TABLE_MAX_ITEMS', 10)


BREADCRUMBS_DEPTH_LEVEL = getattr(settings, 'BREADCRUMBS_DEPTH_LEVEL', 3)


GUARDIAN_STATUS_CHOICES = getattr(settings, 'GUARDIAN_STATUS_CHOICES', (
    ('', 'إختر من القائمة'),
    ('', '')
))


STATUS_CHOICES = getattr(settings, 'STATUS_CHOICES', (
    ('', 'إختر من القائمة'),
    ('new', 'وافد'),
    ('left', 'مغادر'),
    ('dropped', 'منقطع'),
))
