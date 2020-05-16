from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('userLogin/', auth_views.LoginView.as_view(template_name='main/userLogin.html'), name='userLogin'),
    path('userLogout/', auth_views.LogoutView.as_view(template_name='main/userLogout.html'), name='userLogout'),
    path('userRegister/', views.userRegister, name='userRegister'),
    path('movieDetail/', views.movieDetail, name='movieDetail'),
    path('s/', views.resultSearch, name='resultSearch'),
    path('s/action', views.movieList, name='movieList'),
    path('s/<int:pk>/', views.movieDetail, name='movieDetail_with_pk'),
    path('movieUpdate/', views.movieUpdate, name='movieUpdate'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
