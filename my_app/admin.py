from django.contrib import admin
from django.contrib.auth.models import Group
# Register your models here.
from .models import Movie, Twitter

admin.site.site_header = 'Administration'

class MovieAdmin(admin.ModelAdmin):
    list_display = ('movie_title', 'movie_year')
    search_fields = ('movie_title', 'movie_year')
    change_list_template = 'admin/main/movieList.html'

class TwitterAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Movie, MovieAdmin)
admin.site.register(Twitter, TwitterAdmin)
admin.site.unregister(Group)