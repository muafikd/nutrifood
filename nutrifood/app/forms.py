from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import * 
from django.forms import ModelForm, FileInput, Textarea, BooleanField
from django.utils.translation import gettext_lazy as _

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']
        labels = {
            'name': _('Имя пользователя'),
            'username': _('Никнейм пользователя'),
            'email': _('Электронная почта'),
            'password': _('Пароль'),
            'password2': _('Подтверждение пароля')
        }

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'date_of_birth', 'weight', 'height']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'weight': forms.NumberInput(attrs={'step': "0.1"}),
            'height': forms.NumberInput(attrs={'step': "1"})
        }
        labels = {
            'name': 'Имя пользователя',
            'username': 'Никнейм',
            'date_of_birth': 'Дата рождения',
            'weight': 'Вес (кг)',
            'height': 'Рост (см)'
        }

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleImageField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result
    
class ProductForm(ModelForm):
    photos = MultipleImageField()

    class Meta:
        model = Product
        fields = ['name', 'description', 'photos']
        widgets = {
            'description': Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            existing_photos = instance.productphoto_set.all()
            for photo in existing_photos:
                self.fields[f'photo_{photo.id}'] = BooleanField(label='Delete', required=False)
