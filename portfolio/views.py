from .models import Photos
from django.http import Http404
from django.db.models import Q
from utils.pagination import make_pagination
import os
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Count
from django.utils import translation
from django.utils.translation import gettext as _
from .forms import contatoForm
from django.contrib import messages
#from django.core.mail import EmailMessage

PER_PAGE = os.environ.get('PHOTOS_PER_PAGE',7)

class PhotosListViewBase(ListView):
    model = Photos
    paginate_by = None
    context_object_name = 'photos'
    ordering = ['-id']
    template_name = 'pages/home.html'

    def get_queryset(self, *args, **kwargs):
        consulta = super().get_queryset(*args, **kwargs)
        consulta = consulta.filter(
            esta_publicado=True,
            )
        consulta = consulta.select_related('author','category')
        return consulta
    
    def get_context_data(self, *args, **kwargs):
        contexto = super().get_context_data(*args, **kwargs)
        pagina_objeto, range_paginacao = make_pagination(self.request, contexto.get('photos'), PER_PAGE)
        html_language = translation.get_language()
        contexto.update({
            'photos': pagina_objeto,
            'range_paginacao': range_paginacao,
            'html_language': html_language,
        })
        return contexto

class PhotosListViewHome(PhotosListViewBase):
    template_name = 'pages/home.html'

class PhotosListViewHomeAPI(PhotosListViewBase):
    template_name = 'pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        photos = self.get_context_data()['photos']
        photos_lista = photos.object_list.values()

        return JsonResponse(
            list(photos_lista),
            safe=False
        )

class PhotoListViewCategory(PhotosListViewBase):
    template_name = 'pages/category.html'

    def get_context_data(self, *args, **kwargs):
        contexto = super().get_context_data(*args, **kwargs)
        category_translation = _('Category')
        contexto.update({
            'title': f'{category_translation}: {contexto.get("photos")[0].category.nome} | '
        })

        return contexto

    def get_queryset(self, *args, **kwargs):
        consulta = super().get_queryset(*args, **kwargs)
        consulta = consulta.filter(
            esta_publicado=True, 
            category__id=self.kwargs.get('category_id'),
        )

        if not consulta:
            raise Http404()
        
        return consulta

class PhotosListViewSearch(PhotosListViewBase):
    template_name = 'pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q','').strip()
        consulta = super().get_queryset(*args, **kwargs)
        consulta = consulta.filter(
                Q(
                Q(titulo__icontains=search_term)|
                Q(descricao__icontains=search_term),
                ),
                esta_publicado=True,
            )
        
        if not search_term:
            raise Http404()

        return consulta
    
    def get_context_data(self, *args, **kwargs):
        contexto = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q','').strip()
        contexto.update({
            'page_title': f' Procurando por "{search_term}" |',
            'search_term': search_term,
            'aditional_url_query':f'&q={search_term}',
        })
        return contexto

class PhotoDetail(DetailView):
    model = Photos
    context_object_name = 'photo'
    template_name = 'pages/photo-view.html'

    def get_context_data(self, *args, **kwargs):
        contexto = super().get_context_data(*args, **kwargs)
        contexto.update({
            'is_detail_page': True,
        })

        return contexto
    
class PhotoDetailAPI(PhotoDetail):
    def render_to_response(self, context, **response_kwargs):
        photo = self.get_context_data()['photo']
        photo_dictionary = model_to_dict(photo)
        photo_dictionary['criado_em'] = str(photo.criado_em)
        photo_dictionary['atualizado_em'] = str(photo.atualizado_em)

        if photo_dictionary.get('photo_image'):
            photo_dictionary['photo_image'] = self.request.build_absolute_uri()+\
            photo_dictionary['photo_image'].url
        else:
            photo_dictionary['photo_image']= ''

        del photo_dictionary['esta_publicado']
        del photo_dictionary['historia_html']

        return JsonResponse(
            photo_dictionary, 
            safe=False,
        )

def inventario(request, *args, **kwargs):
    photos = Photos.objects.all()

    try:
        photos = Photos.objects.get_publicados()
        photos = photos.select_related('author')
        numero_photos = photos.aggregate(total=Count('id'))
    except ObjectDoesNotExist:
        photos = None

    contexto = {
        'photos': photos,
        'total_photos': numero_photos['total'],
    }
    return render(request, 'pages/inventario.html', context=contexto)

def contact_mail(request):
    form = contatoForm(request.POST or None)

    if str(request.method) == 'POST':
        if form.is_valid():
            nome = form.cleaned_data['name']
            email = form.cleaned_data['email']
            assunto = form.cleaned_data['subject']
            mensagem = form.cleaned_data['message']

            print('MENSAGEM ENVIADA COM SUCESSO!!!')
            print(f'Nome: {nome}')
            print(f'e-mail: {email}')
            print(f'Assunto: {assunto}')
            print(f'Mensage: {mensagem}')

            messages.success(request, 'E-mail enviado com sucesso!!!')

            #Configuração para enviar e-mail em produção
            #mail = EmailMessage(
            #    subject = assunto,
            #    body = nome + '\n' + email + '\n\n' + mensagem,
            #    from_email= 'no-reply@mail.com',
            #    to = ['fmoraes05@gmail.com', 'fmoraes05@outlook.com'],
            #)
            #mail.send()

            form = contatoForm()
        else:
            messages.error(request, 'Erro ao enviar a mensagem...')
            
    context = {
        'form': form,
    }
    return render(request, 'global/partials/contact.html', context)