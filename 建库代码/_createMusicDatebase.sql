-- ﻿DROP DATABASE MUSIC;
CREATE DATABASE MUSIC;

USE MUSIC;

CREATE TABLE SONGS (
  song_id      BIGINT UNSIGNED NOT NULL,
  song_name    VARCHAR(127) NOT NULL,
  resource_url VARCHAR(127) NOT NULL DEFAULT '',
  style        VARCHAR(31),
  is_hot       TINYINT UNSIGNED NOT NULL,
  album_id     BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (song_id)
) CHARACTER SET utf8;

CREATE TABLE ARTISTS (
    artist_id      BIGINT UNSIGNED NOT NULL,
    artist_name    VARCHAR(127) NOT NULL,
    artist_pic_url VARCHAR(127) NOT NULL,
    briefDesc      VARCHAR(8191),
    albums_count   INT UNSIGNED NOT NULL,
    songs_count    INT UNSIGNED NOT NULL,
    PRIMARY KEY (artist_id)
)CHARACTER SET utf8;

CREATE TABLE ALBUMS (
    album_id      BIGINT UNSIGNED NOT NULL,
    album_name    VARCHAR(127) NOT NULL,
    album_pic_url VARCHAR(127) NOT NULL,
    publish_time  BIGINT UNSIGNED NOT NULL,
    description   VARCHAR(8191) NOT NULL,
    company       VARCHAR(127),
    type          VARCHAR(31),
    sub_type      VARCHAR(31),
    artist_id     BIGINT UNSIGNED NOT NULL,
    songs_count   INT UNSIGNED NOT NULL,
		FOREIGN KEY (artist_id) REFERENCES ARTISTS(artist_id)
        ON DELETE CASCADE 
        ON UPDATE CASCADE 
    PRIMARY KEY (album_id)
)CHARACTER SET utf8;

CREATE TABLE USRS(
    usr_id      BIGINT UNSIGNED NOT NULL,
    nickname    VARCHAR(127)  NOT NULL,
    gender      TINYINT NOT NULL,
    birthday    DATETIME,
    province    VARCHAR(31) NOT NULL,
    city        VARCHAR(31) NOT NULL,
    avatar_url  VARCHAR(127) NOT NULL,
    PRIMARY KEY (usr_id)
)CHARACTER SET utf8;

CREATE TABLE PLAYLISTS(
    playlist_id      BIGINT UNSIGNED NOT NULL,
    creator_id       BIGINT UNSIGNED NOT NULL,
    playlist_pic_url VARCHAR(127) NOT NULL,
    PRIMARY KEY (playlist_id)
)CHARACTER SET utf8;


CREATE TABLE Artist_Songs(
    artist_id    BIGINT UNSIGNED NOT NULL,
    song_id      BIGINT UNSIGNED NOT NULL,
    FOREIGN KEY (song_id) REFERENCES SONGS(song_id)
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    FOREIGN KEY (artist_id) REFERENCES ARTISTS(artist_id)
        ON DELETE CASCADE 
        ON UPDATE CASCADE 
)CHARACTER SET utf8;

CREATE TABLE Artist_Hot_Songs(
    artist_id    BIGINT UNSIGNED NOT NULL,
    song_id      BIGINT UNSIGNED NOT NULL,
    FOREIGN KEY (song_id) REFERENCES SONGS(song_id)
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    FOREIGN KEY (artist_id) REFERENCES ARTISTS(artist_id)
        ON DELETE CASCADE 
        ON UPDATE CASCADE 
)CHARACTER SET utf8;

CREATE TABLE Artist_Album(
    artist_id    BIGINT UNSIGNED NOT NULL,
    album_id     BIGINT UNSIGNED NOT NULL,
    FOREIGN KEY (album_id) REFERENCES ALBUMS(album_id)
        ON DELETE CASCADE 
        ON UPDATE CASCADE ,
    FOREIGN KEY (artist_id) REFERENCES ARTISTS(artist_id)
        ON DELETE CASCADE 
        ON UPDATE CASCADE 
)CHARACTER SET utf8;

CREATE TABLE Usr_Liked_Resource(
    usr_id          BIGINT UNSIGNED NOT NULL,
    type_id         INT UNSIGNED NOT NULL 
                    CHECK(type_id in (1, 10, 127, 1270)),  /*appoint to resource type*/
    resource_id     BIGINT UNSIGNED NOT NULL, /*can be song_id, artist_id, album_id, playlist_id*/
    FOREIGN KEY (usr_id) REFERENCES USRS(usr_id)
        ON DELETE CASCADE 
        ON UPDATE CASCADE 
)CHARACTER SET utf8;

CREATE TABLE Playlist_Songs(
    playlist_id      BIGINT UNSIGNED NOT NULL,
    song_id          BIGINT UNSIGNED NOT NULL,
    FOREIGN KEY (song_id) REFERENCES SONGS(song_id)
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    FOREIGN KEY (playlist_id) REFERENCES PLAYLISTS(playlist_id)
        ON DELETE CASCADE 
        ON UPDATE CASCADE
)CHARACTER SET utf8;

