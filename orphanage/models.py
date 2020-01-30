from django.db import models


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
        return self.full_name

    def update_full_name(self):
        self.full_name = self.first_name + ' ' + self.last_name
        self.save(update_fields=['full_name', ])

    @classmethod
    def list(cls):
        list = cls.objects.all()
        return list
