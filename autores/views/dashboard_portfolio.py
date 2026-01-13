from django.views import View
from portfolio.models import Photos
from django.http import Http404
from autores.forms.photo_form import AuthorsPhotoForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(
    login_required(login_url='autores:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardPhotos(View):
    def get_photo(self, id=None):
        my_photo = None

        if id is not None:
            my_photo = Photos.objects.filter(
                esta_publicado = False,
                author = self.request.user,
                pk = id,
            ).first()

            if not my_photo:
                raise Http404()
        
        return my_photo
    
    def render_photo(self, formulary):
        return render(self.request, 'pages/dashboard_photos.html', context={
            'form': formulary,
        })
    
    def get(self, request, id=None):
        #print('Estou usando Class Based Views')
        my_photo = self.get_photo(id)
        
        formulary = AuthorsPhotoForm(instance = my_photo)

        return self.render_photo(formulary)

    def post(self, request, id=None):
        my_photo = self.get_photo(id)
        
        formulary = AuthorsPhotoForm(
            data = request.POST or None,
            files = request.FILES or None,
            instance = my_photo
        )

        if formulary.is_valid():
            photo = formulary.save(commit=False)
            photo.author = request.user
            photo.historia_html = False
            photo.esta_publicado = False

            photo.save()
            messages.success(request, 'Seu trabalho foi salvo com sucesso!!!')
            return redirect(reverse('autores:dashboard_photo_edit', args=(photo.id,)))
        
        return self.render_photo(formulary)
    
@method_decorator(
    login_required(login_url='autores:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardPhotosDelete(DashboardPhotos):
    def post(self, *args, **kwargs):
        my_photo = self.get_photo(self.request.POST.get('id'))

        my_photo.delete()
        messages.success(self.request, 'Trabalho excluído com sucesso!!!')

        return redirect(reverse('autores:dashboard'))