from django.conf import settings


TABLE_SIZE = getattr(settings, 'TABLE_SIZE', 10)


BREADCRUMBS_DEPTH_LEVEL = getattr(settings, 'BREADCRUMBS_DEPTH_LEVEL', 3)


GUARDIAN_STATUS_CHOICES = getattr(settings, 'GUARDIAN_STATUS_CHOICES', (
    ('', 'إختر من القائمة'),
    ('pending', 'في إنتظار الموافقة'),
    ('accepted', 'طلب مقبول'),
    ('accepted', 'طلب مرفوض'),
))


STATUS_CHOICES = getattr(settings, 'STATUS_CHOICES', (
    ('', 'إختر من القائمة'),
    ('new', 'مستجد'),
    ('left', 'مغادر'),
    ('dropped', 'منقطع'),
))
