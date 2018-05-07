from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ficha-articulo/', views.ficha_articulo, name='ficha_articulo'),
    path('landing-page-admin/', views.landing_page_admin, name='landing_page_admin'),
    path('landing-page-pn/', views.landing_page_pn, name='landing_page_pn'),
    path('perfil-usuario-dueno/', views.perfil_usuario_dueno, name='perfil_usuario_dueno'),
]
