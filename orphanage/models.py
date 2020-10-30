import os

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

from orphanage import settings as orphanage_settings


class Child(models.Model):

    class Meta:
        verbose_name = 'طفل'
        verbose_name_plural = 'أطفال'
        ordering = ('first_name', 'last_name')

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
    status = models.CharField('الحالة', max_length=10, choices=orphanage_settings.STATUS_CHOICES, null=True, blank=True)

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

    # def save(self, *args, **kwargs):
    #     if self.full_name != self.first_name + ' ' + self.last_name:
    #         self.update_full_name()
    #     super(Child, self).save(*args, **kwargs)

    @classmethod
    def list(cls, **kwargs):

        filters = Q()
        if 'name' in kwargs:
            name = kwargs['name'][0]
            filters = Q(first_name__icontains=name) | Q(last_name__icontains=name) | Q(full_name__icontains=name)
        if 'ids' in kwargs:
            ids = kwargs['ids']
            filters &= Q(id__in=ids)

        return cls.objects.filter(filters)

    @classmethod
    def import_photos(cls):
        children = cls.objects.all()

        basedir = settings.BASE_DIR
        path = basedir + f'{settings.MEDIA_URL}images/children'
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


class Year(models.Model):
    
    class Meta:
        verbose_name = 'السنة الدراسية'
        verbose_name_plural = 'السنوات الدراسية'
        ordering = ('-year', )
    
    year = models.PositiveSmallIntegerField('السنة', unique=True)

    def __str__(self):
        return f"{self.year}/{self.year + 1}"


class Grade(models.Model):
    
    class Meta:
        verbose_name = 'المستوى الدراسي'
        verbose_name_plural = 'المستويات الدراسية'
    
    title = models.CharField('المستوى', max_length=255)

    def __str__(self):
        return f"{self.title}"

    @classmethod
    def list(cls, **kwargs):

        filters = Q()
        if 'title' in kwargs:
            title = kwargs['title'][0]
            filters = Q(title__icontains=title)

        return cls.objects.filter(filters)


class Registration(models.Model):
    
    class Meta:
        verbose_name = 'الملف الدراسي'
        verbose_name_plural = 'الملفات الدراسية'
    
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    year = models.ForeignKey(Year, on_delete=models.PROTECT)
    s1_mark = models.DecimalField('نقطة الدورة الأولى', max_digits=4, decimal_places=2)
    s2_mark = models.DecimalField('نقطة الدورة الثانية', max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.child}"


class Subject(models.Model):
    
    class Meta:
        verbose_name = 'المادة الدراسية'
        verbose_name_plural = 'المواد الدراسية'

    title = models.CharField('العنوان', max_length=255)
    code = models.CharField('الرقم', max_length=10)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"


class Mark(models.Model):
    
    class Meta:
        verbose_name = 'النقطة'
        verbose_name_plural = 'النقط'

    registration = models.ForeignKey(Registration, on_delete=models.PROTECT)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    mark = models.DecimalField('النقطة', max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.registration} - {self.subject}"


class Guardian(User):
    
    class Meta:
        verbose_name = 'الكافل'
        verbose_name_plural = 'الكفلاء'

    picture = models.ImageField('الصورة', upload_to='images/guardians', null=True, blank=True)
    phone_number = models.CharField('رقم الهاتف', max_length=25, null=True, blank=True)
    status = models.CharField('الحالة', max_length=10, choices=orphanage_settings.GUARDIAN_STATUS_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
