from django.urls import path, re_path

from . import views

app_name = 'myapi'
urlpatterns = [
    path('', views.index, name='index'),
    path('album/', views.album, name='album'),
    path('song/', views.song, name='song'),
    # re_path('music/album', views.album, name='album'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]