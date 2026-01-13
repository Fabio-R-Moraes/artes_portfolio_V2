from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.PhotosListViewHome.as_view(), name='photos-home'),
    path('category/<int:category_id>/', views.PhotoListViewCategory.as_view(), name='category'),
    path('photo/<int:pk>/', views.PhotoDetail.as_view(), name='photos-photo'),
    path('photo/search/', views.PhotosListViewSearch.as_view(), name='search'),
    path('trabalhos/API/v1/', views.PhotosListViewHomeAPI.as_view(), name='trabalhos_api_v1'),
    path('trabalhos/API/v1/<int:pk>/', views.PhotoDetailAPI.as_view(), name='trabalho_api_v1_detalhe'),
    path('photos/inventario/', views.inventario, name='inventario'),
    path('photos/contact.html', views.contact_mail, name="contact_mail"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)