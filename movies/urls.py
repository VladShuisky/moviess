from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.MovieView.as_view(), name='movies'),
    path('<slug:slug>/', views.MovieDetailView.as_view(), name='moviedetail'),
    path('review/<int:pk>/', views.AddReview.as_view(), name='add_review'),
]


if settings.DEBUG:
    if settings.MEDIA_ROOT:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)