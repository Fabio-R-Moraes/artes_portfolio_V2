from django import forms
from portfolio.models import Photos
from utils.django_forms import novos_atributos
from utils.strings import is_a_positicve_number
from django.core.exceptions import ValidationError
from collections import defaultdict
from django.utils.translation import gettext_lazy as _

class AuthorsPhotoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.my_errors = defaultdict(list)

        novos_atributos(self.fields.get('historia'), 'class', 'span-2')

    class Meta:
        model = Photos
        fields = 'titulo', 'descricao', 'category', 'preco', 'historia', 'photo_image'

        labels = {
            'titulo': _('Title'),
            'descricao': _('Description'),
            'category': _('Category'),
            'preco': _('Value'),
            'historia': _('History'),
            'photo_image': _('Work'),
        }

        widgets = {
            'photo_image': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            )
        }

        def clean(self, *args, **kwargs):
            super_clean = super().clean(*args, **kwargs)

            cleaned_data = self.cleaned_data
            titulo = cleaned_data.get('titulo')
            descricao = cleaned_data.get('descricao')

            if titulo == descricao:
                self.my_errors['titulo'].append('Título e Descrição não podem ser iguais...')
                self.my_errors['descricao'].append('Descrição e título não podem ser iguais...')

            if self.my_errors:
                raise ValidationError(self.my_errors)
            
            return super_clean
        
        def clean_titulo(self):
            titulo = self.cleaned_data.get('titulo')

            if len(titulo) < 5:
                self.my_errors['titulo'].append('O título deve ter mais de 5 caracteres!!!')

            return titulo
        
        def clean_preco(self):
            field_name = 'preco'
            field_value = self.cleaned_data.get(field_name)

            if not is_a_positicve_number(field_value):
                self.my_errors[field_name].append('O preço precisa ser positivo... por favor!!!')

            return field_value