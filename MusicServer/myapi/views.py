from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
import pymysql.cursors
import json

def search_songs_by_song_id(song_id):
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='x',
                             db='music',
                             cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:

        song_sql = "SELECT * FROM Songs WHERE song_id=%s;"
        album_sql = "SELECT * FROM Albums WHERE album_id=%s;"
        artist_sql = "SELECT * FROM Artists WHERE artist_id=%s;"
        artist_by_song_sql = "SELECT artist_id FROM Artist_Songs WHERE song_id=%s;"
        
        cursor.execute(song_sql, song_id)
        songs = cursor.fetchone()

        cursor.execute(album_sql, songs['album_id'])
        album = cursor.fetchone()

        cursor.execute(artist_by_song_sql, song_id)
        artist_ids = cursor.fetchall()
        artists = []
        for artist_id in artist_ids:
            cursor.execute(artist_sql, artist_id['artist_id'])
            artists.append(cursor.fetchone())

        songs['album'] = album 
        songs['artists'] = artists  

    connection.close()
    return {'songs': songs, 'code': 200}

def search_album_by_album_id(album_id):
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='x',
                             db='music',
                             cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        album_sql = "SELECT * FROM Albums WHERE album_id=%s;"
        song_sql = "SELECT * FROM Songs WHERE song_id=%s;"
        artist_sql = "SELECT * FROM Artists WHERE artist_id=%s;"
        songs_album_sql = "SELECT * FROM Songs WHERE album_id=%s;"
        artist_by_album_sql = "SELECT artist_id FROM Artist_Album WHERE album_id=%s;"

        cursor.execute(album_sql, album_id)
        album = cursor.fetchone()

        cursor.execute(songs_album_sql, album_id)
        songs = cursor.fetchall()

        cursor.execute(artist_by_album_sql, album_id)
        artist_ids = cursor.fetchall()

        artists = []
        for artist_id in artist_ids:
            cursor.execute(artist_sql, artist_id['artist_id'])
            artists.append(cursor.fetchone())
        
        album['artists'] = artists
    connection.close() 
    return {'songs': songs, 'album': album, 'code': 200}



def search_artist_by_artist_id(artist_id):
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='x',
                             db='music',
                             cursorclass=pymysql.cursors.DictCursor)
    artist_sql = "SELECT * FROM Artists WHERE artist_id=%s;"
    album_sql = "SELECT * FROM Albums WHERE album_id=%s;"
    song_sql = "SELECT * FROM Songs WHERE song_id=%s;"
    hot_songs_by_artist_sql = "SELECT * FROM Artist_Hot_Songs WHERE artist_id=%s;"
    # songs_artists_sql = "SELECT song_id FROM Artist_Songs WHERE artist_id=%s;"
    album_by_artist_sql = "SELECT album_id FROM Artist_Album WHERE artist_id=%s;"
    with connection.cursor() as cursor:
        cursor.execute(artist_sql, artist_id)
        artist = cursor.fetchone()

        cursor.execute(album_by_artist_sql, artist_id)
        album_ids = cursor.fetchall()
        
        cursor.execute(hot_songs_by_artist_sql, artist_id)
        song_ids = cursor.fetchall()

        albums = []
        for album_id in album_ids:
            cursor.execute(album_sql, album_id['album_id'])
            albums.append(cursor.fetchone())
        
        songs = []
        for song_id in song_ids:
            cursor.execute(song_sql, song_id['song_id'])
            songs.append(cursor.fetchone())
        
        # artists['hot_songs'] = songs 

    connection.close() 
    return {'artist': artist, 'hot_albums': albums, 'hot_songs': songs, 'code': 200}



# Create your views here.
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)
    
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


def album_add(request):
    received_data = json.loads(request.body.decode('utf-8'))
    
