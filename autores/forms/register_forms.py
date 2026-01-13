from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import senhaForte
from django.utils.translation import gettext_lazy as _

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    password2 = forms.CharField(
        required=True,
        label= _('Repeat your password'),
        error_messages={
            'required': 'A senha não pode ser vazia...',
        },
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme sua senha',
        }),
        validators=[senhaForte],
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
        }

        help_texts = {
            'email': 'Digite seu melhor e-mail',
        }

        error_messages = {
            'first_name': {
                'required': 'Escreva seu nome',
            },
            'last_name': {
                'required': 'Preciso do seu sobrenome',
            },
            'username': {
                'required': 'Esse campo NÃO pode ser vazio',
            },
            'email': {
                'required': 'Sem o seu e-mail o seu e-mail o cadastro NÃO pode ser feito',
            },
            'password': {
                'required': 'A senha NÃO pode ser vazia',
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Seu primeiro nome',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Seu sobrenome',
            }),
            'username': forms.TextInput(attrs={
                'placeholder': 'Pense num usuário',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Pense numa senha',
            }),
            
        }

    def clean(self):
        dados = super().clean()
        password = dados.get('password')
        password2 = dados.get('password2')

        if password != password2:
            raise ValidationError({
                'password': 'As senhas devem ser iguais...',
                'password2': 'As senhas devem ser iguais...',
            })
        
    def clean_email(self):
        email = self.cleaned_data.get('email','')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'Esse e-mail já está sendo usado!!!', code='Invalid',
            )