from datetime import datetime

from django import forms
from django.forms import ModelForm

from orphanage.models import Child
from orphanage.widgets import DateWidget, ImageWidget


class ConnectionForm(forms.Form):

    username = forms.CharField(label='إسم المستخدم', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'إسم المستخدم'}
    ))
    password = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'كلمة المرور'}
    ))


class ChildForm(ModelForm):

    birthday = forms.DateField(input_formats=['%d/%m/%Y', ],
                               widget=DateWidget(format='%d/%m/%Y', attrs={'class': 'form-control'}))

    class Meta:
        model = Child

        fields = [
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

    # def clean(self):
    #     # cleaned_data = super(ChildForm, self).clean()
    #     bd = self.data['birthday']
    #     print('cleaning birthday - bd =', bd)
    #     # try:
    #     if True:
    #         birthday = datetime.strptime(bd, '%d/%m/%Y')
    #         print('birthday:', birthday)
    #         return bd
    #     # except:
    #     #     return None
