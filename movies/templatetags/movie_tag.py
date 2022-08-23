from django import template
from movies.models import Category, Movie, Actor


register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.inclusion_tag('movies/tags/last_movies.html')
def get_last_movies():
    last_movies = Movie.objects.order_by('id')[:5]
    return {'last_movies': last_movies}

    
@register.simple_tag()
def get_forward_actors():
    return Actor.objects.all()[:2]