from django import forms
from django.forms import ModelForm

from orphanage.models import Child
from orphanage.widgets import DateInput


class ConnectionForm(forms.Form):

    username = forms.CharField(label='إسم المستخدم', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'إسم المستخدم'}
    ))
    password = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'كلمة المرور'}
    ))


class ChildForm(ModelForm):

    class Meta:
        model = Child

        fields = [
            'first_name',
            'last_name',
            'picture',
            'sex',
            'grade',
            'birthday',
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
            'picture': forms.FileInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(choices=Child.SEX_CHOICES, attrs={'class': 'form-control'}),
            'grade': forms.TextInput(attrs={'class': 'form-control'}),
            'birthday': DateInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'village': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'bed_position': forms.TextInput(attrs={'class': 'form-control'}),
            'shoo_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'vision': forms.TextInput(attrs={'class': 'form-control'}),
            'orphan_side': forms.Select(choices=Child.ORPHAN_CHOICES, attrs={'class': 'form-control'}),
            'chronic_disease': forms.TextInput(attrs={'class': 'form-control'}),
            'hobby': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
        }
