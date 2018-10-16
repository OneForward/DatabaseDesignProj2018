# 模拟网易云音乐数据库管理系统

--------


文件结构
│  JSON_POST_FORMAT.json
│  README.md
│  
├─MusicServer
│  │  manage.py
│  │  
│  ├─MusicServer
│  │  │  settings.py
│  │  │  urls.py
│  │  │  wsgi.py
│  │  │  __init__.py
│  │  │  
│  │  └─
│  │          
│  └─myapi
│      │  admin.py
│      │  apps.py
│      │  models.py
│      │  tests.py
│      │  urls.py
│      │  views.py
│      │  __init__.py
│      └─ 
│              
└─建库代码
    │  createAlbumsTables.py
    │  createArtistsTables.py
    │  createSongArtistAlbumsTables.py
    │  createSongsTables.py
    │  create_utils.py
    │  README.md
    │  requirements.txt
    │  _createMusicDatebase.sql
    │  
    └─脱库代码
            json_parse_and_save.py
            json_parse_and_save_album_all_songs.py
            searchPy.py
            top_artists_100.py

            
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
