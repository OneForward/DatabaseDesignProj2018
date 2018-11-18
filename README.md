# 模拟网易云音乐数据库管理系统

--------

<pre>
文件结构
│  README.md
│  tree.txt
│  
├─SQL建库代码
│  │  createAlbumsTables.py
│  │  createArtistsTables.py
│  │  createSongArtistAlbumsTables.py
│  │  createSongsTables.py
│  │  create_utils.py
│  │  database_json.rar
│  │  README.md
│  │  requirements.txt
│  │  _createMusicDatebase.sql
│  │  
│  └─脱库代码
│          addPlaylists.py
│          addPlaylistsSongs.py
│          addPlaylistsSongs2.py
│          addSongInfo.py
│          json_parse_artists_and_save_albums.py
│          json_parse_artist_album_and_save_all_songs.py
│          json_top_artists_100.py
│          parseAlbumid_then_add_everything.py
│          parseSongid_then_add_everything.py
│          parseSongid_then_add_everything_2.py
│          README.md
│          search.py
│          top_playlists.json
│          utils.py
│          
├─用户使用前端GUI
│  │  .browserslistrc
│  │  .eslintrc.js
│  │  .gitignore
│  │  api.json
│  │  babel.config.js
│  │  package-lock.json
│  │  package.json
│  │  postcss.config.js
│  │  README.md
│  │  
│  ├─public
│  │  │  favicon.ico
│  │  │  index.html
│  │  │  manifest.json
│  │  │  robots.txt
│  │  │  
│  │  └─img
│  │      └─icons
│  │              android-chrome-192x192.png
│  │              android-chrome-512x512.png
│  │              apple-touch-icon-120x120.png
│  │              apple-touch-icon-152x152.png
│  │              apple-touch-icon-180x180.png
│  │              apple-touch-icon-60x60.png
│  │              apple-touch-icon-76x76.png
│  │              apple-touch-icon.png
│  │              favicon-16x16.png
│  │              favicon-32x32.png
│  │              msapplication-icon-144x144.png
│  │              mstile-150x150.png
│  │              safari-pinned-tab.svg
│  │              
│  └─src
│      │  App.vue
│      │  main.css
│      │  main.js
│      │  registerServiceWorker.js
│      │  router.js
│      │  store.js
│      │  
│      ├─assets
│      │      logo.png
│      │      
│      ├─components
│      │  │  PlayerBar.vue
│      │  │  
│      │  ├─Browser
│      │  │      SearchBar.vue
│      │  │      
│      │  ├─Common
│      │  │      AlbumItem.vue
│      │  │      AlbumsList.vue
│      │  │      ArtistItem.vue
│      │  │      ArtistsList.vue
│      │  │      Loading.vue
│      │  │      PlaylistItem.vue
│      │  │      PlaylistsList.vue
│      │  │      SongItem.vue
│      │  │      SongsList.vue
│      │  │      
│      │  └─Details
│      │          AlbumSidebar.vue
│      │          ArtistHeader.vue
│      │          
│      ├─modules
│      │      browser.js
│      │      collection.js
│      │      home.js
│      │      player.js
│      │      
│      ├─plugins
│      │      vuetify.js
│      │      
│      ├─services
│      │      browser.js
│      │      collection.js
│      │      details.js
│      │      home.js
│      │      _global_config.json
│      │      
│      ├─util
│      │      util.js
│      │      
│      └─views
│          │  Browser.vue
│          │  Collection.vue
│          │  Details.vue
│          │  Home.vue
│          │  Setting.vue
│          │  
│          └─Details
│                  AlbumDetails.vue
│                  ArtistDetails.vue
│                  
└─管理员后台GUI
    │  browser.cpp
    │  browser.h
    │  browserwidget.ui
    │  connectionwidget.cpp
    │  connectionwidget.h
    │  dialog.ui
    │  info.h
    │  main.cpp
    │  qsqlconnectiondialog.cpp
    │  qsqlconnectiondialog.h
    │  qsqlconnectiondialog.ui
    │  README.md
    │  sqlbrowser.pro
    │  
    └─images
            example1.png
            example2.png

</pre>           
注：
1. 本项目为2018-2019年秋季学期CS400数据库原理与应用大作业
2. 本项目由四个主体构成：SQL建库代码、管理后台界面、前端界面开发、用户端服务器，github源码链接接分别为

[SQL建库代码+管理员后台界面](https://github.com/OneForward/DatabaseDesignProj2018)，[用户使用前端界面](https://github.com/tomoya06/pp-music-player),  [用户使用端服务器](https://github.com/tomoya06/NeteaseCloudMusicAPIV2_mysql)

3. ER模型

![ER模型](images/ER_white.png?raw=true)

4. 制表结构
![制表结构](images/UML_white.png?raw=true)