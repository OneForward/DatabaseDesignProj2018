from django.urls import path, re_path

from . import views

app_name = 'myapi'
urlpatterns = [
    path('', views.index, name='index'),
    path('fetchpost/', views.fetchpost, name='fetchpost'),
    path('album/', views.album, name='album'),
    path('song/', views.song, name='song'),
    path('artist/', views.artist, name='artist'),
    # path('album/add', views.album_add, name='album_add'),
    # path('artist/add', views.artist_add, name='artist_add'),
    # path('song/add', views.song_add, name='song_add'),
]