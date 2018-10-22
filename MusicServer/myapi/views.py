from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
import json
from .utils import *
from .parseAlbumid_then_add_everything import parse_album_id_and_add_everything
from .parseSongid_then_add_everything import parse_song_id_and_add_everything
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt 
def fetchpost(request):
    print(request)
    # print(request.GET)
    # print(request.POST)

    received_data = json.loads(json.loads(request.body.decode('utf-8')))
    if received_data['type'] == 1:
        song_id = received_data['id']
        parse_song_id_and_add_everything(song_id)
    if received_data['type'] == 2:
        album_id = received_data['id']
        parse_album_id_and_add_everything(album_id)
    if received_data['type'] == 3:
        album_id = received_data['id']
        update_song(received_data['data'])
    return HttpResponse("OK") 
    
def index(request):
    print(request)
    print(request.GET)
    return HttpResponse("You are looking at index") 

def album(request):
    query = request.GET
    album_id = query.get('id', 0)
    if album_id == 0:
        return HttpResponse("fetch error")
    else:
        data = search_album_by_album_id(album_id)
        return JsonResponse(data)

def song(request):
    query = request.GET
    song_id = query.get('id', 0)
    if song_id == 0:
        return HttpResponse("fetch error")
    else:
        data = search_songs_by_song_id(song_id)
        return JsonResponse(data)


def artist(request):
    query = request.GET
    artist_id = query.get('id', 0)
    if artist_id == 0:
        return HttpResponse("fetch error")
    else:
        data = search_artist_by_artist_id(artist_id)
        return JsonResponse(data)
