from django import forms


class ConnectionForm(forms.Form):

    username = forms.CharField(label='إسم المستخدم', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'إسم المستخدم'}
    ))
    password = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'كلمة المرور'}
    ))
