from django.urls import path, re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url


urlpatterns = [
    path('', views.index, name='login'),
    re_path(r'^ficha-articulo/(((?P<article_name>[-\w]+)/)?id_(?P<article_id>\d+)/)$', views.ficha_articulo, name='ficha_articulo'),
    path('landing-page-admin/', views.landing_page_admin, name='landing_page_admin'),
    path('landing-page-admin/usuarios', views.landing_page_admin_usuarios, name='landing_page_admin_usuarios'),
    path('landing-page-admin/grilla', views.landing_page_admin_grilla, name='landing_page_admin_grilla'),
    path('landing-page-admin/grillav', views.landing_page_admin_grillav, name='landing_page_admin_grillav'),
    path('landing-page-admin/grillac', views.landing_page_admin_grillac, name='landing_page_admin_grillac'),
    path('landing-page-admin/grillap', views.landing_page_admin_grillap, name='landing_page_admin_grillap'),
    path('landing-page-admin/articuloespacio', views.landing_page_admin_articuloespacio, name='landing_page_admin_articuloespacio'),
    path('landing-page-pn/', views.landing_page_pn, name='landing_page_pn'),
    path('landing-page-pn/articulos/', views.landing_page_pn_articulos, name='landing_page_pn_articulos'),
    path('landing-page-pn/espacios/', views.landing_page_pn_espacios, name='landing_page_pn_espacios'),
    path('perfil-usuario-dueno/', views.perfil_usuario_dueno, name='perfil_usuario_dueno'),
    path('perfil-usuario-dueno-espacios/', views.perfil_usuario_dueno_espacios, name='perfil_usuario_dueno_espacios'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),

    path('create-article/', views.create_article, name='create_article'),
    url(r'^updatearticle/(?P<pk>\d+)/$', views.ArticleUpdate.as_view(), name='updatearticle'),
    path('deletearticle/<int:Article_id>', views.deletearticle, name='deletearticle'),
    path('deletespace/<int:Space_id>', views.deletespace, name='deletespace'),

   path('modificarPendientes/', views.modificarPendientes, name='modificarPendientes'),

    path('dyn_styles/', views.dyn_styles, name='dyn_styles')
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)