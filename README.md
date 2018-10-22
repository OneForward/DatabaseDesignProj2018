# 模拟网易云音乐数据库管理系统

--------

<pre>
文件结构
│  .gitignore
│  JSON_POST_FORMAT.json
│  README.txt
│  
├─MusicServer
│  │  manage.py
│  │  
│  ├─MusicServer
│  │      settings.py
│  │      urls.py
│  │      wsgi.py
│  │      __init__.py
│  │      
│  └─myapi
│          admin.py
│          apps.py
│          models.py
│          post_test.py
│          tests.py
│          urls.py
│          views.py
│          __init__.py
│          
├─SQLBackendGUI
│      browser.cpp
│      browser.h
│      browserwidget.ui
│      connectionwidget.cpp
│      connectionwidget.h
│      dialog.ui
│      info.h
│      main.cpp
│      qsqlconnectiondialog.cpp
│      qsqlconnectiondialog.h
│      qsqlconnectiondialog.ui
│      sqlbrowser.pro
│      
└─建库代码
    │  createAlbumsTables.py
    │  createArtistsTables.py
    │  createSongArtistAlbumsTables.py
    │  createSongsTables.py
    │  create_utils.py
    │  database_json.rar
    │  README.md
    │  requirements.txt
    │  _createMusicDatebase.sql
    │  
    └─脱库代码
            json_parse_artists_and_save_albums.py
            json_parse_artist_album_and_save_all_songs.py
            json_top_artists_100.py
            parseAlbumid_then_add_everything.py
            parseSongid_then_add_everything.py
            README.md
            search.py
            utils.py

</pre>           
注：
1. JSON_POST_FORMAT.json里面写明了双方约定执行增删改操作时的POST请求格式
2. 在`MusicServer/`路径下执行 `python manage.py runserver`可以建立本地数据库的服务器, 注意连接数据库时需要修改`MusicServer/MusicServer/settings.py`中的DATABASE条目的相关参数
3. 本地API接口如下

localhost:8000/myapi

歌曲信息
/song?id=

歌手信息
/artist?id=

专辑信息
/album?id=

4. ER模型

![ER模型](_report/src/ER.png?raw=true)

5. 制表结构
![制表结构](_report/src/UML.png?raw=true)