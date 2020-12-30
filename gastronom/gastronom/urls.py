"""gastronom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from gastronom.settings import MEDIA_URL, MEDIA_ROOT
#from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView


# def trigger_error(request):
#     division_by_zero = 1 / 0

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('notifications/', include('notifications.urls')),
    path('user_profile/', include('user_profile.urls')),
    path('catalog/', include('catalog.urls')),
    path('product/', include('product.urls')),
    path('comments/', include('comments.urls')),
    path('cart/', include('cart.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    #path('login/', auth_views.LoginView.as_view(redirect_field_name='/catalog/catalog/'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(redirect_field_name='/catalog/catalog/'), name='logout'),
    path('info/', include('info.urls')),
    path('tinymce/', include('tinymce.urls')),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)

