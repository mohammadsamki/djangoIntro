from django.urls import include, path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('book/', index, name='bookList'), # ''= ( mean root page)
    #  book_detail url
    path('book/<int:pk>/', detail, name='book_detail'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('staff/', staffPage, name='staffPage'),
    path('normalUser/', userPage, name='userPage'),
    path('manager/', managerPage, name='managerPage'),
    path('authorlist/', author_list, name='author_list'),
    path('userBooks/', userBooks, name='userBooks'),
        path('playlists/', user_playlists, name='user_playlists'),
    path('playlists/<int:playlist_id>/', playlist_videos, name='playlist_videos'),

path('social-auth/', include('social_django.urls', namespace='social')),
path('register/', userRegister, name='register'),
]
# urls.py


