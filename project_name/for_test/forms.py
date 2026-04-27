from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import Lesson, LessonMaterial, Profile

User = get_user_model()

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'description')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class LessonMaterialForm(forms.ModelForm):
    class Meta:
        model = LessonMaterial
        fields = ('title', 'material_type', 'text', 'file', 'url')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'material_type': forms.Select(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        material_type = cleaned_data.get('material_type')
        text = cleaned_data.get('text')
        file = cleaned_data.get('file')
        url = cleaned_data.get('url')

        if material_type == LessonMaterial.MATERIAL_TEXT:
            if not text:
                self.add_error('text', 'Для текстового материала нужно заполнить текст.')
            cleaned_data['file'] = None
            cleaned_data['url'] = ''

        elif material_type == LessonMaterial.MATERIAL_FILE:
            if not file:
                self.add_error('file', 'Для файлового материала нужно загрузить файл.')
            cleaned_data['text'] = ''
            cleaned_data['url'] = ''

        elif material_type == LessonMaterial.MATERIAL_VIDEO:
            if not url and not file:
                self.add_error('url', 'Для видео нужно указать ссылку или загрузить файл.')
                self.add_error('file', 'Для видео нужно указать ссылку или загрузить файл.')
            cleaned_data['text'] = ''

        elif material_type == LessonMaterial.MATERIAL_PRESENTATION:
            if not file:
                self.add_error('file', 'Для презентации нужно загрузить файл.')
            cleaned_data['text'] = ''
            cleaned_data['url'] = ''

        return cleaned_data

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar',)