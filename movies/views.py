from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ReviewForm
from .models import *
from django.views.generic import ListView, DetailView
from django.views import View
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .serializers import ActorSerializer, UserSerializer
from blog.models import CustomUser
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm


class ActorView(DetailView):
    template_name = 'movies/actor.html'
    model = Actor
    slug_field = 'name'

class AuthorisationView(DetailView):
    def post(self, request):
            username = request.POST['name']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('movies:movies'))
            else:
                return HttpResponse('Ошибка')

def loginpage(request):
    form = RegistrationForm()
    template = 'movies/authorisation.html'
    return render(request, template, {'form': form})

def login_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('movies:movies'))
    

class MovieView(ListView):
    # context_object_name = 'movies'
    model = Movie
    # queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movielist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movies'] = Movie.objects.filter(draft=False)
        context['user'] = self.request.user
        return context

    # def get(self, request, *args, **kwargs):
    #     return render(request, self.template_name, self.get_context_data)

    # def get (self, request):
    #     movies = Movie.objects.all()
    #     template = 'movies/movielist.html'
    #     context = {'movies': movies}  
    #     return render(request, template, context)


class MovieDetailView(DetailView):
    template_name = 'movies/moviedetail.html'
    model = Movie
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['actors'] = 
        # context['directors'] = ', '.join([x.name for x in self.object.directors.all()])
        context['genres'] = ', '.join([x.name for x in self.object.genres.all()])
        return context


class AddReview(View):
    def post(self, request, pk):    # pk это movie.id который мы передали из шаблонизатора в форму, данные из которой отправились пост запросом
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(pk=pk)
        if request.user.is_authenticated:
            if form.is_valid():
                form = form.save(commit=False) # теперь можно добавить в форму поле напрямую
                if request.POST.get('parent', None):
                    form.parent_id = int(request.POST.get('parent'))
                form.movie = movie # movie_id это колонка для привязку фильма к review по id фильма. Здесь мы его напрямую указываем через Pk
                form.save()  # экземпляр Review создан
            return redirect(movie.get_absolute_url())
        else: 
            return HttpResponse('Вы не зарегистрированы в сети')


# django rest framework
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    # def get(self, request, slug):
    #     movie = get_object_or_404(Movie, url=slug)
    #     template = 'movies/moviedetail.html'
    #     directors = ', '.join([x.name for x in movie.directors.all()])
    #     actors = ', '.join([x.name for x in movie.actors.all()])
    #     context = {'movie': movie, 'directors': directors, 'actors': actors}
    #     return render(request, template, context)
    

def zalupa(request):
    return HttpResponse('hahhahahah')