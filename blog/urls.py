from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexViev.as_view(), name='index'),
    path('<int:post_id>/', views.detail, name='detail'),
    path('login/', views.loginpage, name='loginpage'),
    path('authorization/', views.authorisation, name='authorisation'),
    path('logout/', views.login_out, name='logout'),
    path('registration/', views.registration, name='registration'),
    path('create_post/', views.postcreatingpage, name='postcreatingpage'),
    path('publicate/', views.publicate, name='publicate'),
]


# if settings.DEBUG:
#     if settings.MEDIA_ROOT:
#         urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)