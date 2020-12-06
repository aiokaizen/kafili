from django.conf import settings


# Application settings
TABLE_SIZE = getattr(settings, 'TABLE_SIZE', 10)

BREADCRUMBS_DEPTH_LEVEL = getattr(settings, 'BREADCRUMBS_DEPTH_LEVEL', 3)


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


# Grade settings
GRADE_LEVEL_CHOICES = getattr(settings, 'GRADE_LEVEL_CHOICES', (
    (1, 'الأول'),
    (2, 'الثاني'),
    (3, 'الثالث'),
    (4, 'الرابع'),
    (5, 'الخامس'),
    (6, 'السادس'),
    (7, 'السابع'),
))

# Guardian settings
GUARDIAN_STATUS_CHOICES = getattr(settings, 'GUARDIAN_STATUS_CHOICES', (
    ('', 'إختر من القائمة'),
    ('pending', 'في إنتظار الموافقة'),
    ('accepted', 'طلب مقبول'),
    ('accepted', 'طلب مرفوض'),
))
