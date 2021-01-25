import os

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

from orphanage.services import calculate_decision
from orphanage import settings as orphanage_settings


class Child(models.Model):

    class Meta:
        verbose_name = 'طفل'
        verbose_name_plural = 'أطفال'
        ordering = ('first_name', 'last_name')

    # TODO: add this field in insert and update templates and forms
    subscription_id = models.PositiveIntegerField('رقم الإنخراط', unique=True, null=True, blank=True)
    first_name = models.CharField('الإسم', max_length=255)
    last_name = models.CharField('اللقب', max_length=255)
    full_name = models.CharField('الإسم الكامل', max_length=255, null=True, blank=True)
    picture = models.ImageField('الصورة', upload_to='images/students', null=True, blank=True)
    sex = models.CharField('الجنس', max_length=1, choices=orphanage_settings.SEX_CHOICES, null=True, blank=True)
    grade = models.CharField('المستوى الدراسي', max_length=10, null=True, blank=True)
    birthday = models.DateField('تاريخ الإزدياد', null=True, blank=True)
    phone_number = models.CharField('رقم الهاتف', max_length=25, null=True, blank=True)
    village = models.CharField('الدوار', max_length=155, null=True, blank=True)
    weight = models.PositiveSmallIntegerField('الوزن', null=True, blank=True)
    height = models.PositiveSmallIntegerField('القامة', null=True, blank=True)
    bed_position = models.CharField('تموضع السرير', max_length=15, null=True, blank=True)
    shoo_size = models.CharField('مقاس الحذاء', max_length=8, null=True, blank=True)
    vision = models.CharField('الرؤية', max_length=55, null=True, blank=True)
    orphan_side = models.CharField('اليتم', choices=orphanage_settings.ORPHAN_CHOICES, max_length=10, null=True, blank=True)
    chronic_disease = models.CharField('مرض مزمن', max_length=55, null=True, blank=True)
    hobby = models.CharField('الهواية', max_length=25, null=True, blank=True)
    status = models.CharField('الحالة', max_length=10, choices=orphanage_settings.STATUS_CHOICES, default="", blank=True)

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

    def get_students(self):
        return self.student_set.all()

    def get_student(self, year=None):
        if not year:
            year = Year.objects.first()
        students = self.get_students()
        if students:
            return students.get(grade__year=year)
        else:
            return None

    def create_child(self):
        self.save()

    def update_child(self):
        self.save()

    def delete_child(self):
        self.save()

    def delete(self, *args, **kwargs):
        super(Student, self).delete(*args, **kwargs)

    @classmethod
    def delete_children(cls, children):
        success, message = True, "لقد تمت العملية بنجاح."
        for child in children:
            success, msg = child.delete_child()
            if not success:
                message = msg
                break
        return success, message

    @classmethod
    def list(cls, **kwargs):

        filters = Q()
        if 's_query' in kwargs:
            name = kwargs['s_query'][0]
            filters = Q(first_name__icontains=name) | Q(last_name__icontains=name) | Q(full_name__icontains=name)
        if 'name' in kwargs:
            name = kwargs['name'][0]
            filters = Q(first_name__icontains=name) | Q(last_name__icontains=name) | Q(full_name__icontains=name)
        if 'ids' in kwargs:
            ids = kwargs['ids']
            filters &= Q(id__in=ids)

        if 'subscription_id' in kwargs and kwargs['subscription_id'][0]:
            subscription_id = kwargs['subscription_id'][0]
            filters = Q(subscription_id=subscription_id)
        if 'sex' in kwargs and kwargs['sex'][0]:
            sex = kwargs['sex'][0]
            filters = Q(sex=sex)
        if 'village' in kwargs and kwargs['village'][0]:
            village = kwargs['village'][0]
            filters = Q(village__icontains=village)
        if 'shoo_size' in kwargs and kwargs['shoo_size'][0]:
            shoo_size = kwargs['shoo_size'][0]
            filters = Q(shoo_size__icontains=shoo_size)
        if 'vision' in kwargs and kwargs['vision'][0]:
            vision = kwargs['vision'][0]
            filters = Q(vision__icontains=vision)
        if 'orphan_side' in kwargs and kwargs['orphan_side'][0]:
            orphan_side = kwargs['orphan_side'][0]
            filters = Q(orphan_side=orphan_side)
        if 'chronic_disease' in kwargs and kwargs['chronic_disease'][0]:
            chronic_disease = kwargs['chronic_disease'][0]
            filters = Q(chronic_disease__icontains=chronic_disease)
        if 'hobby' in kwargs and kwargs['hobby'][0]:
            hobby = kwargs['hobby'][0]
            filters = Q(hobby__icontains=hobby)
        if 'status' in kwargs and kwargs['status'][0]:
            status = kwargs['status'][0]
            filters = Q(status=status)

        return cls.objects.filter(filters)

    @classmethod
    def import_photos(cls):
        students = cls.objects.all()

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
                student = students.get(id=value)
                if not student.picture or 1:
                    img_path = f'images/children/{img}'
                    student.picture = img_path
                    student.save(update_fields=['picture', ])
                    print(student)
                    success_import_count += 1

            except ObjectDoesNotExist:
                not_imported.append(img)

        err_message = ''
        if not_imported:
            non_importees = ''
            for img in not_imported:
                non_importees += img + '; '
            err_message = f'({len(not_imported)}/{len(os.listdir(path))}) Images were not imported: {non_importees}'

        message = f"لقد تم إستيراد {success_import_count} صورة."
        return True, message, err_message


class Student(models.Model):

    class Meta:
        verbose_name = 'تلميذ'
        verbose_name_plural = 'تلاميذ'
        ordering = ('child', )

    child = models.ForeignKey(Child, verbose_name="الطفل", on_delete=models.PROTECT)
    grade = models.ForeignKey('Grade', verbose_name="المستوى الدراسي", on_delete=models.PROTECT)
    s1_mark = models.DecimalField('نقطة الدورة الأولى', max_digits=4, decimal_places=2, null=True, blank=True)
    s1_decision = models.CharField('ميزة الدورة الأولى', max_length=2, choices=orphanage_settings.STUDENT_DECISION_CHOICES, default="", blank=True)
    s2_mark = models.DecimalField('نقطة الدورة الثانية', max_digits=4, decimal_places=2, null=True, blank=True)
    s2_decision = models.CharField('ميزة الدورة الثانية', max_length=2, choices=orphanage_settings.STUDENT_DECISION_CHOICES, default="", blank=True)
    year_mark = models.DecimalField('معدل السنة', max_digits=4, decimal_places=2, null=True, blank=True)
    year_decision = models.CharField('ميزة السنة', max_length=2, choices=orphanage_settings.STUDENT_DECISION_CHOICES, default="", blank=True)
    status = models.CharField('الحالة', max_length=10, choices=orphanage_settings.STATUS_CHOICES, default='passed', blank=True)

    # Functions
    def __str__(self):
        return f"{self.child} - {self.grade}"

    def save(self, grade=None, *args, **kwargs):
        if not self.id:
            self.grade = grade
        
        if 's1_mark' in kwargs['update_fields'] or 's2_mark' in kwargs['update_fields'] or 'year_mark' in kwargs['update_fields']:
            self.update_decisions()
        super(Student, self).save(*args, **kwargs)
    
    def update_decisions(self):
        self.s1_decision = calculate_decision(self.s1_mark)
        self.s2_decision = calculate_decision(self.s2_mark)
        self.year_decision = calculate_decision(self.year_mark)
        super(Student, self).save()

    def delete(self, *args, **kwargs):
        super(Student, self).delete(*args, **kwargs)

    @classmethod
    def delete_students(cls, students):
        res, message = True, "لقد تمت العملية بنجاح."
        for student in students:
            student.delete()
        return res, message

    @classmethod
    def list(cls, grade, **kwargs):

        filters = Q(grade=grade)
        if 's_query' in kwargs:
            name = kwargs['s_query'][0]
            filters &= Q(child__first_name__icontains=name) | Q(child__last_name__icontains=name) | Q(child__full_name__icontains=name)
        if 'name' in kwargs:
            name = kwargs['name'][0]
            filters &= Q(child__first_name__icontains=name) | Q(child__last_name__icontains=name) | Q(child__full_name__icontains=name)
        if 'ids' in kwargs:
            ids = kwargs['ids']
            filters &= Q(id__in=ids)

        if 'subscription_id' in kwargs and kwargs['subscription_id'][0]:
            subscription_id = kwargs['subscription_id'][0]
            filters = Q(child__subscription_id=subscription_id)
        if 'status' in kwargs and kwargs['status'][0]:
            status = kwargs['status'][0]
            filters = Q(status=status)

        return cls.objects.filter(filters)


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
        ordering = ['level']
        unique_together = ('level', 'year')
    
    title = models.CharField('المستوى', max_length=255)
    level = models.PositiveSmallIntegerField('المستوى')
    year = models.ForeignKey(Year, on_delete=models.PROTECT)
    mark_ceiling = models.PositiveSmallIntegerField('أعلى نقطة ممكنة', default=10)

    def __str__(self):
        return f"{self.title}"
    
    def get_grade_title_from_level(self):
        level = [title for lvl, title in orphanage_settings.GRADE_LEVEL_CHOICES if lvl == self.level][0]
        return f"{level} إبتدائي"
    
    def students(self):
        return self.student_set.all()
    
    def students_count(self):
        return self.students().count()
    
    def create_grade(self, year):
        try:
            self.title = self.get_grade_title_from_level()
            success, message = True, f"لقد تمت إضافة المستوى {self.title} بنجاح."
            self.year = year
            self.save()
        except IntegrityError:
            success, message = False, f"هذا المستوى مسجل بالفعل في هذه السنة الدراسية."
        return success, message
    
    def update_grade(self):
        try:
            self.title = self.get_grade_title_from_level()
            success, message = True, f"لقد تمت تحديث المستوى بنجاح."
            self.save()
        except IntegrityError:
            success, message = False, f"هذا المستوى مسجل بالفعل في هذه السنة الدراسية."
        return success, message
    
    def delete_grade(self):
        grade = self.title
        self.delete()
        return True, f"لقد تمت إزالة المستوى {grade} بنجاح."
    
    @classmethod
    def delete_grades(cls, grades):
        success, message = True, f"لقد تمت إزالة المستويات بنجاح."
        for grade in grades:
            success, msg = grade.delete_grade()
            if not success:
                message = msg
                break
        return success, message
        
    @classmethod
    def list(cls, year, **kwargs):

        filters = Q(year=year)
        if 'title' in kwargs:
            title = kwargs['title'][0]
            filters &= Q(title__icontains=title)

        return cls.objects.filter(filters)


# class Registration(models.Model):
    
#     class Meta:
#         verbose_name = 'الملف الدراسي'
#         verbose_name_plural = 'الملفات الدراسية'
    
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
#     year = models.ForeignKey(Year, on_delete=models.PROTECT)
#     s1_mark = models.DecimalField('نقطة الدورة الأولى', max_digits=4, decimal_places=2)
#     s2_mark = models.DecimalField('نقطة الدورة الثانية', max_digits=4, decimal_places=2)
#     year_mark = models.DecimalField('معدل السنة', max_digits=4, decimal_places=2)

#     def __str__(self):
#         return f"{self.student}"


class Subject(models.Model):
    
    class Meta:
        verbose_name = 'المادة الدراسية'
        verbose_name_plural = 'المواد الدراسية'

    title = models.CharField('العنوان', max_length=255)
    code = models.CharField('الرقم', max_length=10)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    coeff = models.PositiveSmallIntegerField('المعامل', default=0)

    def __str__(self):
        return f"{self.title}"
    
    def create_subject(self, grade):
        success, message = True, f"لقد تمت إضافة  {self.title} بنجاح."
        self.grade = grade
        self.save()
        return success, message
    
    def delete_subject(self):
        subject = self.title
        self.delete()
        return True, f"لقد تمت إزالة {subject} بنجاح."
        
    @classmethod
    def list(cls, grade, **kwargs):

        filters = Q(grade=grade)
        if 'title' in kwargs:
            title = kwargs['title'][0]
            filters &= Q(title__icontains=title)
        if 'code' in kwargs:
            code = kwargs['code'][0]
            filters &= Q(code__icontains=code)

        return cls.objects.filter(filters)


class Mark(models.Model):
    
    class Meta:
        verbose_name = 'النقطة'
        verbose_name_plural = 'النقط'

    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    mark = models.DecimalField('النقطة', max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.student} - {self.subject}"


class Guardian(User):
    
    class Meta:
        verbose_name = 'الكافل'
        verbose_name_plural = 'الكفلاء'

    picture = models.ImageField('الصورة', upload_to='images/guardians', null=True, blank=True)
    first_name_ar = models.CharField('الإسم الشخصي بالعربية', max_length=57, default='', blank=True)
    last_name_ar = models.CharField('الإسم العائلي بالعربية', max_length=57, default='', blank=True)
    phone_number = models.CharField('رقم الهاتف', max_length=25, null=True, blank=True)
    status = models.CharField('الحالة', max_length=10, choices=orphanage_settings.GUARDIAN_STATUS_CHOICES, default='pending', blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def save(self, *args, **kwargs):
        if self.id:
            self.change(*args, **kwargs)
        else:
            self.create(*args, **kwargs)
    
    def create(self, *args, **kwargs):
        super(Guardian, self).save(self, *args, **kwargs)
    
    def change(self, *args, **kwargs):
        super(Guardian, self).save(self, *args, **kwargs)
