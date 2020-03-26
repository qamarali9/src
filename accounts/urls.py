"""tweet URL Configuration

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

from django.urls import path, re_path

#from .views import tweet_detail_view, tweet_detail_view, tweet_list_view
from .views import (
    # TweetCreateView,
    # TweetDetailView, 
    # TweetListView,
    # TweetUpdateView,
    # TweetDeleteView
    UserDetailView,
    UserFollowView
    )

app_name = "accounts"

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', tweet_list_view, name='home'),
    #path('<int:pk>/', tweet_detail_view, name='home'),
    # path('', RedirectView.as_view(url='/'), name='list'), # /tweet/ --> /
    # path('search/', TweetListView.as_view(), name='list'), # /tweet/search/
    # path('create/', TweetCreateView.as_view(), name='create'), # /tweet/create/
    re_path(r'^(?P<username>[\w.@+-]+)/$', UserDetailView.as_view(), name='detail'), # /username
    re_path(r'^(?P<username>[\w.@+-]+)/follow/$', UserFollowView.as_view(), name='follow'), # /username/follow
    # path('<int:pk>/', TweetDetailView.as_view(), name='detail'), # /tweet/2/
    # path('<int:pk>/update/', TweetUpdateView.as_view(), name='update'), # /tweet/1/update/
    # path('<int:pk>/delete/', TweetDeleteView.as_view(), name='delete'), # /tweet/1/delete/
]