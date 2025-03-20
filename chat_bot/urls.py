from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('chat',views.text_genaration,  name='gpt'),
    path('bot', views.text_generatior, name='chat'),
    path("register", views.register, name="register"),
    path("", views.custom_login, name="login"),
    path("logout", views.custom_logout, name="logout"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)