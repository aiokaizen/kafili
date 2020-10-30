from datetime import datetime

from django import forms
from django.forms import ModelForm

from orphanage.models import Child, Grade, Year
from orphanage.widgets import DateWidget, ImageWidget


class ConnectionForm(forms.Form):

    username = forms.CharField(label='إسم المستخدم', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'إسم المستخدم'}
    ))
    password = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'كلمة المرور'}
    ))


class ChildForm(ModelForm):

    birthday = forms.DateField(label='تاريخ الإزدياد', input_formats=['%d/%m/%Y', ],
                               widget=DateWidget(format='%d/%m/%Y', attrs={'class': 'form-control'}))

    class Meta:
        model = Child

        fields = [
            'subscription_id',
            'first_name',
            'last_name',
            'picture',
            'sex',
            'grade',
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
            'picture': ImageWidget(),
            'sex': forms.Select(choices=Child.SEX_CHOICES, attrs={'class': 'form-control'}),
            'grade': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'village': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'bed_position': forms.TextInput(attrs={'class': 'form-control'}),
            'shoo_size': forms.TextInput(attrs={'class': 'form-control'}),
            'vision': forms.TextInput(attrs={'class': 'form-control'}),
            'orphan_side': forms.Select(choices=Child.ORPHAN_CHOICES, attrs={'class': 'form-control'}),
            'chronic_disease': forms.TextInput(attrs={'class': 'form-control'}),
            'hobby': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
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


class GradeForm(ModelForm):

    class Meta:
        model = Grade
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }


class YearForm(ModelForm):

    class Meta:
        model = Year
        fields = '__all__'
        widgets = {
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
        }
