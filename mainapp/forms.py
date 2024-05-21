from django import forms
# from django.forms import widgets
from django.utils.deconstruct import deconstructible

from .models import ArticleModel, Category, Comments


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."

    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise forms.ValidationError(
                self.message, code=self.code, params={"value": value})


class ArticleForm(forms.ModelForm):
    cat = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Выберите категорию'
    )

    class Meta:
        model = ArticleModel
        fields = [
            'name', 'description', 'content', 'photo', 'is_published',
        ]

        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control mr-0 ml-auto"}),
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 2, 'class': "form-control mr-0 ml-auto"}),
            'content': forms.Textarea(attrs={'cols': 40, 'rows': 5, 'class': "form-control mr-0 ml-auto"}),
            # {'content': forms.Textarea(attrs={'cols': 40, 'rows':5})},
            # {'content': forms.Textarea(attrs={'cols': 40, 'rows':5})},
            # {'content': forms.Textarea(attrs={'cols': 40, 'rows':5, 'class': 'col-sm-3 col-form-label text-right tm-color-primary'})},

        }

        def clean_name(self):
            name = self.cleaned_data['name']
            if len(name) > 50:
                raise forms.ValidationError('Длинна превышает 50 символов')

            return name


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        label='Имя',
        widget=forms.TextInput(attrs={"class": "form-control mr-0 ml-auto"}),
    )
    email = forms.EmailField(
        label='E-mail',
        widget=forms.TextInput(attrs={"class": "form-control mr-0 ml-auto"}),
    )
    subject = forms.CharField(
        label='Тема',
        widget=forms.TextInput(attrs={"class": "form-control mr-0 ml-auto"}),
    )
    message = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea(
            attrs={'cols': 40, 'rows': 5, 'class': "form-control mr-0 ml-auto"})
    )


class CommentsForm(forms.ModelForm):
    # comment = forms.CharField(
    #     widget=forms.Textarea(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Введите текст комментария',
    #             'rows': 5,
    #         }
    #     ),
    # )

    class Meta:
        model = Comments
        fields = ['text']
