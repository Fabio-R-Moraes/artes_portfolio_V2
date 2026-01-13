from django import forms

class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    username = forms.CharField(
        label='Usuário',
    )

    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput()
    )