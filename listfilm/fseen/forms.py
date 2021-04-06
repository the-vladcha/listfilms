from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField

from .models import MyUser


class LoginForm(forms.ModelForm):
    username = forms.CharField(help_text='')
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f"Пользователь с логином {username} не найден в системе.")
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(help_text='')
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    phone_number = PhoneNumberField(required=False)
    email = forms.EmailField(required=True)
    captcha = ReCaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердите пароль'
        self.fields['phone_number'].label = 'Номер телефона'
        self.fields['email'].label = 'Email'
        self.fields['captcha'].label = ''
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Данный почтовый адрес уже зарегистрирован')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if MyUser.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError(f'Данный телефонный номер уже зарегистрирован')
        return phone_number

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Имя {username} занято')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'email', 'phone_number']


