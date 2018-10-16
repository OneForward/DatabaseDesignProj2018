# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Albums(models.Model):
    album_id = models.BigIntegerField(primary_key=True)
    album_name = models.CharField(max_length=127)
    album_pic_url = models.CharField(max_length=127)
    songs_count = models.PositiveIntegerField()

    class Meta:
        managed = True
        db_table = 'albums'


class Artistalbumsongs(models.Model):
    artist = models.ForeignKey('Artists', models.DO_NOTHING)
    song = models.ForeignKey('Songs', models.DO_NOTHING)
    is_hot = models.PositiveIntegerField()
    album = models.ForeignKey(Albums, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'artistalbumsongs'


class Artists(models.Model):
    artist_id = models.BigIntegerField(primary_key=True)
    artist_name = models.CharField(max_length=127)
    artist_pic_url = models.CharField(max_length=127)
    decription_url = models.CharField(max_length=127)
    albums_count = models.PositiveIntegerField()
    songs_count = models.PositiveIntegerField()

    class Meta:
        managed = True
        db_table = 'artists'


class Playlists(models.Model):
    playlist_id = models.BigIntegerField(primary_key=True)
    creator_id = models.BigIntegerField()
    playlist_pic_url = models.CharField(max_length=127)

    class Meta:
        managed = True
        db_table = 'playlists'


class Playlistsongs(models.Model):
    playlist = models.ForeignKey(Playlists, models.DO_NOTHING)
    song = models.ForeignKey('Songs', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'playlistsongs'


class Songs(models.Model):
    song_id = models.BigIntegerField(primary_key=True)
    song_name = models.CharField(max_length=127)
    lyric_url = models.CharField(max_length=127)
    resource_url = models.CharField(max_length=127)
    album_id = models.BigIntegerField()

    class Meta:
        managed = True
        db_table = 'songs'


class Usrlikedresource(models.Model):
    usr = models.ForeignKey('Usrs', models.DO_NOTHING)
    type_id = models.PositiveIntegerField()
    resource_id = models.BigIntegerField()

    class Meta:
        managed = True
        db_table = 'usrlikedresource'


class Usrs(models.Model):
    usr_id = models.BigIntegerField(primary_key=True)
    nickname = models.CharField(max_length=127)
    gender = models.IntegerField()
    birthday = models.DateTimeField(blank=True, null=True)
    province = models.CharField(max_length=31)
    city = models.CharField(max_length=31)
    avatar_url = models.CharField(max_length=127)

    class Meta:
        managed = True
        db_table = 'usrs'
