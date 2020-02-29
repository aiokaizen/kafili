import os

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.files import File
from django.db import models
from django.db.models import Q

from kafili.settings import MEDIA_URL


class Child(models.Model):

    class Meta:
        verbose_name = 'طفل'
        verbose_name_plural = 'أطفال'
        ordering = ['first_name', 'last_name']

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

    STATUS_CHOICES = (
        ('', 'إختر من القائمة'),
        ('new', 'وافد'),
        ('left', 'مغادر'),
        ('dropped', 'منقطع'),
    )

    # TODO: add this field in insert and update templates and forms
    subscription_id = models.PositiveIntegerField('رقم الإنخراط', unique=True, null=True, blank=True)
    first_name = models.CharField('الإسم', max_length=255)
    last_name = models.CharField('اللقب', max_length=255)
    full_name = models.CharField('الإسم الكامل', max_length=255, null=True, blank=True)
    picture = models.ImageField('الصورة', upload_to='images/children', null=True, blank=True)
    sex = models.CharField('الجنس', max_length=1, choices=SEX_CHOICES, null=True, blank=True)
    grade = models.CharField('المستوى الدراسي', max_length=10, null=True, blank=True)
    birthday = models.DateField('تاريخ الإزدياد', null=True, blank=True)
    phone_number = models.CharField('رقم الهاتف', max_length=25, null=True, blank=True)
    village = models.CharField('الدوار', max_length=155, null=True, blank=True)
    weight = models.PositiveSmallIntegerField('الوزن', null=True, blank=True)
    height = models.PositiveSmallIntegerField('القامة', null=True, blank=True)
    bed_position = models.CharField('تموضع السرير', max_length=15, null=True, blank=True)
    shoo_size = models.CharField('مقاس الحذاء', max_length=8, null=True, blank=True)
    vision = models.CharField('الرؤية', max_length=55, null=True, blank=True)
    orphan_side = models.CharField('اليتم', choices=ORPHAN_CHOICES, max_length=10, null=True, blank=True)
    chronic_disease = models.CharField('مرض مزمن', max_length=55, null=True, blank=True)
    hobby = models.CharField('الهواية', max_length=25, null=True, blank=True)
    status = models.CharField('الحالة', max_length=10, choices=STATUS_CHOICES, null=True, blank=True)

    # Functions
    def __str__(self):
        return self.full_name if self.full_name else ''

    def get_short_address(self):
        return 'دوار ' + self.village + '، جماعة زرقطن' if self.village else ''

    def get_address(self):
        return 'دوار ' + self.village + '، جماعة زرقطن، قيادة التوامة، عمالة تاحناوت' if self.village else ''

    def update_full_name(self):
        self.full_name = self.first_name + ' ' + self.last_name
        self.save(update_fields=['full_name', ])

    @classmethod
    def list(cls, **kwargs):

        filters = Q()
        if 'name' in kwargs:
            name = kwargs['name'][0]
            filters = Q(first_name__contains=name) | Q(last_name__contains=name) | Q(full_name__contains=name)
        if 'ids' in kwargs:
            ids = kwargs['ids']
            filters &= Q(id__in=ids)

        return cls.objects.filter(filters)

    @classmethod
    def import_photos(cls):
        children = cls.objects.all()

        basedir = settings.BASE_DIR
        path = basedir + f'{MEDIA_URL}images/children'
        if not os.path.exists(path):
            os.mkdir(path)
        not_imported = []
        success_import_count = 0

        for img in os.listdir(path):
            try:
                value = img.split('.')[0]

                if not value.isdigit():
                    continue
                child = children.get(id=value)
                if not child.picture or 1:
                    img_path = f'images/children/{img}'
                    child.picture = img_path
                    child.save(update_fields=['picture', ])
                    print(child)
                    success_import_count += 1

            except ObjectDoesNotExist:
                not_imported.append(img)

        err_message = ''
        if not_imported:
            non_importees = ''
            for img in not_imported:
                non_importees += img + '; '
            err_message = ('warning', f'({len(not_imported)}/{len(os.listdir(path))})',
                           f'Images were not imported: {non_importees}')

        message = ('success', f"{success_import_count} images were imported.")
        return True, [message, err_message]

