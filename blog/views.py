from audioop import reverse
from email.policy import HTTP
import http
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Post
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from .models import CustomUser
from django.views import View
from .forms import RegistrationForm

class IndexViev(View):
    def get(self, request):
        if request.user.is_authenticated:
            print(request.user.id)
            posts = Post.objects.filter(draft=False)
            context = {'posts': posts, 'user': request.user}
            template = 'blog/index.html'
            return render(request, template , context)
        else:
            return HttpResponseRedirect(reverse('blog:loginpage'))



# def index(request):
#     if request.user.is_authenticated:
#         print(request.user.id)
#         posts = Post.objects.filter(draft=False)
#         context = {'posts': posts, 'user': request.user}
#         template = 'blog/index.html'
#         return render(request, template , context)
#     else:
#         return HttpResponseRedirect(reverse('blog:loginpage'))


def detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    template = 'blog/detail.html'
    context = {'post': post}
    return render(request, template, context)

def loginpage(request):
    form = RegistrationForm()
    template = 'blog/login.html'
    return render(request, template, {'form': form})


def authorisation(request):
    username = request.POST['name']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        print(reverse('blog:index'))
        return HttpResponseRedirect(reverse('blog:index'))
    else:
        return HttpResponse('Ошибка')

def login_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('blog:loginpage'))


def registration(request):
    username = request.POST['name']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is None:
        registrated_user = CustomUser.objects.create_user(username=username, password=password)
        registrated_user.save()
        login(request, registrated_user)
        return HttpResponseRedirect(reverse('blog:index'))
    else:
        return HttpResponse('Такой пользователь уже зарегистрирован, залогиньтесь')

def postcreatingpage(request):
    return render(request, 'blog/postcreatingpage.html', {})

def publicate(request):
    if request.user.is_authenticated:
        post_title = request.POST['post_title']
        post_text = request.POST['post_text']
        post = Post.objects.create(title=post_title, text=post_text, author=request.user)
        post.save()
        return HttpResponseRedirect(reverse('blog:index'))
    else:
        return HttpResponse('Ошибка')




###Старые views на основе функций

# def index(request):
#     if request.user.is_authenticated:
#         print(request.user.id)
#         posts = Post.objects.filter(draft=False)
#         context = {'posts': posts, 'user': request.user}
#         template = 'blog/index.html'
#         return render(request, template , context)
#     else:
#         return HttpResponseRedirect(reverse('blog:loginpage'))
        