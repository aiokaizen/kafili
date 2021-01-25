from datetime import datetime

from django import forms

from orphanage import settings as orphanage_settings
from orphanage.models import Child, Student, Grade, Subject, Year, Guardian
from orphanage.widgets import DateWidget, ImageWidget


class ConnectionForm(forms.Form):

    username = forms.CharField(label='إسم المستخدم', widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg', 'placeholder': 'إسم المستخدم', 'aria-invalid': 'true'}
    ))
    password = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-lg', 'placeholder': 'كلمة المرور', 'aria-invalid': 'true'}
    ))


class RegistrationForm(forms.ModelForm):
    
    class Meta:
        model = Guardian
        fields = [
            'first_name',
            'first_name_ar',
            'last_name',
            'last_name_ar',
            'phone_number',
            'email'
        ]

        widgets = {
            'first_name_ar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الإسم الشخصي'}),
            'last_name_ar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الإسم العائلي'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الهاتف'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'البريد الإلكتروني'}),
        }


class ChildForm(forms.ModelForm):

    birthday = forms.DateField(
        label='تاريخ الإزدياد', input_formats=['%d/%m/%Y', ],
        widget=DateWidget(format='%d/%m/%Y', attrs={'class': 'form-control'})
    )

    class Meta:
        model = Child

        fields = [
            'subscription_id',
            'first_name',
            'last_name',
            'picture',
            'sex',
            'phone_number',
            'village',
            'weight',
            'height',
            'bed_position',
            'shoo_size',
            'vision',
            'orphan_side',
            'chronic_disease',
            'hobby',
            'status',
        ]

        widgets = {
            'subscription_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'picture': ImageWidget(attrs={'class': 'custom-file-input'}),
            'sex': forms.Select(choices=orphanage_settings.SEX_CHOICES, attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'village': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'bed_position': forms.TextInput(attrs={'class': 'form-control'}),
            'shoo_size': forms.TextInput(attrs={'class': 'form-control'}),
            'vision': forms.TextInput(attrs={'class': 'form-control'}),
            'orphan_side': forms.Select(choices=orphanage_settings.ORPHAN_CHOICES, attrs={'class': 'form-control'}),
            'chronic_disease': forms.TextInput(attrs={'class': 'form-control'}),
            'hobby': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        sub_id = self.cleaned_data.get('subscription_id')
        count = len(Child.objects.filter(subscription_id=sub_id))
        exists = True if (count > 1 and self.instance.id) or (count > 0 and not self.instance.id) else False
        try:
            if not sub_id or int(sub_id) < 1 or exists:
                self.add_error('subscription_id', ".رقم الإنخراط يجب أن يكون رقما موجب. و أن يكون غير مكرر")
        except ValueError:
            self.add_error('subscription_id', ".رقم الإنخراط يجب أن يكون رقما موجب. و أن يكون غير مكرر")
        return cleaned_data


class ChildFilterForm(forms.Form):

    subscription_id = forms.IntegerField(label="رقم التسجيل", widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    name = forms.CharField(label="الإسم الكامل", widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    sex = forms.ChoiceField(label="الجنس", choices=orphanage_settings.SEX_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    village = forms.CharField(label="الدوار", widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    shoo_size = forms.CharField(label="مقاس الحذاء", widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    vision = forms.CharField(label="الرؤية", widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    orphan_side = forms.ChoiceField(label="اليتم", choices=orphanage_settings.ORPHAN_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    chronic_disease = forms.CharField(label="مرض مزمن", widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    hobby = forms.CharField(label="الهواية", widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    status = forms.CharField(label="الحالة", widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)


class StudentForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = [
            'child', 's1_mark', 's2_mark', 'year_mark', 'status',
        ]

        widgets = {
            'child': forms.Select(attrs={'class': 'form-control select2'}),
            's1_mark': forms.NumberInput(attrs={'class': 'form-control'}),
            's2_mark': forms.NumberInput(attrs={'class': 'form-control'}),
            'year_mark': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_s1_mark(self):
        mark = self.cleaned_data['s1_mark']
        ceiling = self.instance.grade.mark_ceiling
        if mark and mark > ceiling:
            raise forms.ValidationError(f'نقطة غير مقبولة, المرجو إدخال قيمة موجبة أصغر من أو تساوي {ceiling}')
        return mark

    def clean_s2_mark(self):
        mark = self.cleaned_data['s2_mark']
        ceiling = self.instance.grade.mark_ceiling
        if mark and mark > ceiling:
            raise forms.ValidationError(f'نقطة غير مقبولة, المرجو إدخال قيمة موجبة أصغر من أو تساوي {ceiling}')
        return mark

    def clean_year_mark(self):
        mark = self.cleaned_data['year_mark']
        ceiling = self.instance.grade.mark_ceiling
        if mark and mark > ceiling:
            raise forms.ValidationError(f'نقطة غير مقبولة, المرجو إدخال قيمة موجبة أصغر من {ceiling}')
        return mark


class StudentFilterForm(forms.Form):

    subscription_id = forms.IntegerField(label="رقم التسجيل", widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    name = forms.CharField(label="الإسم الكامل", widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    status = forms.CharField(label="الحالة", widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)


class GradeForm(forms.ModelForm):

    class Meta:
        model = Grade
        fields = ('level', )
        widgets = {
            'level': forms.Select(choices=orphanage_settings.GRADE_LEVEL_CHOICES, attrs={'class': 'form-control'}),
        }


class YearForm(forms.ModelForm):

    class Meta:
        model = Year
        fields = '__all__'
        widgets = {
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
        }


# Subject forms
class SubjectForm(forms.ModelForm):
    
    class Meta:
        model = Subject

        fields = ['title', 'code', 'coeff']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'coeff': forms.NumberInput(attrs={'class': 'form-control'}),
        }
