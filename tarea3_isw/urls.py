from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='login'),
    path('ficha-articulo/', views.ficha_articulo, name='ficha_articulo'),
    path('landing-page-admin/', views.landing_page_admin, name='landing_page_admin'),
    path('landing-page-pn/', views.landing_page_pn, name='landing_page_pn'),
    path('landing-page-pn/articulos/', views.landing_page_pn_articulos, name='landing_page_pn_articulos'),
    path('landing-page-pn/espacios/', views.landing_page_pn_espacios, name='landing_page_pn_espacios'),
    path('perfil-usuario-dueno/', views.perfil_usuario_dueno, name='perfil_usuario_dueno'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
