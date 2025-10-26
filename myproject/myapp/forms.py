from django.forms import ModelForm
from .models import Post


from django.contrib.auth.models import User
from django import forms

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'category', 'image']
        


#Форма для регистрации в блоге
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password2'):
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data