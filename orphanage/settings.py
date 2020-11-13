from django.conf import settings


# Application settings
TABLE_SIZE = getattr(settings, 'TABLE_SIZE', 10)

BREADCRUMBS_DEPTH_LEVEL = getattr(settings, 'BREADCRUMBS_DEPTH_LEVEL', 3)


# Guardian settings
GUARDIAN_STATUS_CHOICES = getattr(settings, 'GUARDIAN_STATUS_CHOICES', (
    ('', 'إختر من القائمة'),
    ('pending', 'في إنتظار الموافقة'),
    ('accepted', 'طلب مقبول'),
    ('accepted', 'طلب مرفوض'),
))


# Child settings
SEX_CHOICES = (
    ('', 'إختر من القائمة'),
    ('m', 'ذكر'),
    ('f', 'أنثى')
)

ORPHAN_CHOICES = (
    ('', 'إختر من القائمة'),
    ('mother', 'الأم'),
    ('father', 'الأب'),
    ('both', 'الأم و الأب')
)

STATUS_CHOICES = getattr(settings, 'STATUS_CHOICES', (
    ('', 'إختر من القائمة'),
    ('new', 'وافد'),
    ('left', 'مغادر'),
    ('dropped', 'منقطع'),
))


# Student settings
STUDENT_STATUS_CHOICES = getattr(settings, 'STUDENT_STATUS_CHOICES', (
    ('', 'إختر من القائمة'),
    ('new', 'مستجد'),
    ('passed', 'متأهل'),
    ('repeated', 'مكرر'),
))
