"""twitter_ly URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static

from tweets.views import TweetListView
from tweets.api.views import SearchAPIView
from .views import home, SearchView

from accounts.views import UserRegistrationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TweetListView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),
    path('tags/',include(('hashtags.urls', 'hashtags'), namespace='hashtags')),
    path('tweet/',include(('tweets.urls', 'tweets'), namespace='tweets')),
    path('api/tweet/',include(('tweets.api.urls', 'tweets/api'), namespace='tweets-api')),
    path('api/search/',SearchAPIView.as_view(), name='search-api'),
    path('api/hashtag/',include(('hashtags.api.urls', 'hashtags/api'), namespace='hashtags-api')),
    path('api/',include(('accounts.api.urls', 'accounts/api'), namespace='profiles-api')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', UserRegistrationView.as_view(), name='Register'),
    path('',include(('accounts.urls', 'accounts'), namespace='profiles')),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)