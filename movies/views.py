from urllib import request
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
from .forms import RegistrationForm, RatingForm
from django.db.models import Q
from django.http import JsonResponse
from django import forms
from django.core.paginator import Paginator

class GenreYear:
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values('year').order_by('-year')



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
    

class MovieView(ListView, GenreYear):
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movielist.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movies'] = self.queryset
        context['user'] = self.request.user
        return context

    # def get(self, request, *args, **kwargs):
    #     return render(request, self.template_name, self.get_context_data)

    # def get (self, request):
    #     movies = Movie.objects.all()
    #     template = 'movies/movielist.html'
    #     context = {'movies': movies}  
    #     return render(request, template, context)


class MovieDetailView(DetailView, GenreYear):
    template_name = 'movies/moviedetail.html'
    model = Movie
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = ', '.join([x.name for x in self.object.genres.all()])
        context['user'] = self.request.user
        context['star_form'] = RatingForm()
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
    

class FilterMoviesView(GenreYear, ListView):
    template_name = 'movies/movielist.html'

    def get_queryset(self):
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movies'] = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) | 
            Q(genres__in=self.request.GET.getlist('genre'))).distinct()
        print(self.request.GET)
        print(context)
        return context


class JsonFilterView(ListView):
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) | 
            Q(genres__in=self.request.GET.getlist('genre'))).distinct().values('title', 'tagline', 'url', 'poster')
        for el in queryset:
            print(el)
        return queryset

    def get(self, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({'movies': queryset}, safe=False)


class addRatingView(View):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        print('запрос пост произведерн')
        form = RatingForm(request.POST)
        print(request.POST)   # в форму вставляются данные полученные с фронтенда методом fetch
        if form.is_valid() and request.user.username != '':
                Rating.objects.update_or_create(
                    ip=self.get_client_ip(request),
                    movie_id=int(request.POST.get('movie')),  # айди фильма из скрытого инпута формы
                    defaults={'star_id': int(request.POST.get('star'))} 
                )
                return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)
            


## метод get_or_create ищет обьект по полям которые ппередаются в аргументы
## но по полю который передается в defaults он не ищет!!!
## однако в случае ненахождения данного обьекта он создаст новый обьект и включит туда поле, переданное в словаре defaults