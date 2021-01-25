"""edXRegistration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from registration import views
# from django.urls import path, include
# from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # url(r'^$', home.as_view(), name='home'),
    url(r'^$', views.home, name='home'),
    url(r'^register/', views.register, name='register'),
    url(r'^enroll/', views.enroll, name='enroll'),
    url(r'^confirm/', views.enroll, name='confirm'),
    url(r'^crispy_register/', views.crispy_register, name='crispy_register'),

    # path('', views.home, name='home'),
    # path('treasure/', views.treasure, name='treasure'),
    # path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]
