from django import forms

class contatoForm(forms.Form):
    name = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='E-mail', max_length=100)
    subject = forms.CharField(label='Assunto', max_length=120)
    message = forms.CharField(label='Mensagem', widget=forms.Textarea())