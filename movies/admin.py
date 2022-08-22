from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from django import forms
from django.forms import TextInput, Textarea, CharField
from django.db import models

django_models = [RatingStar, Rating]

for model in django_models:
    admin.site.register(model)


from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Movie

class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Movie
        fields = '__all__'


class ReviewInLine(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ('name', 'email')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_image', 'date_of_birth')
    list_display_links = ('name','get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="160">')

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'country', 'world_premiere', 'get_poster', 'draft')
    list_filter = ('category', 'year', 'country')
    search_fields = ('title',)
    inlines = [ReviewInLine, ]
    save_on_top = True
    form = MovieAdminForm
    save_as = True
    list_editable = ('draft',)
    fieldsets = (
        (None, {'fields': ('title', 'tagline', 'year', 'country')}),
        (None, {'fields': ('description', 'directors', 'actors')}),
        (None, {'fields': ('poster', 'genres', 'world_premiere')}),
        (None, {'fields': ('budget', 'fees_in_usa', 'fess_in_world', 'category', 'url', 'draft')}),

    )
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'150'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }

    def get_poster(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="50" height="70">')

@admin.register(Reviews)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'parent', 'movie')
    list_filter = ('movie',)
    search_fields = ('name', 'movie')
    readonly_fields = ('name', 'email')

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(MovieShots)
class MovieShotAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'get_image', 'movie')
    list_display_links = ('get_image',)
    list_filter = ('movie',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="160" height="100">')