环境：python3， mysql

需要运行网易云数据库API接口
`https://binaryify.github.io/NeteaseCloudMusicApi/#/`

依次运行如下代码脱库，数据文件保存至路径`../database_json/`下
1. top_artists_100.py
2. json_parse_artists_and_save_albums.py
3. json_parse_artist_album_and_save_all_songs.py

辅助脚本：
1. `python parseAlbumid_then_add_everything.py -a/--albumid []`可以自动向数据库添加专辑,
专辑里的所有音乐以及专辑艺人, 并保存相关数据在路径`../database_json/`下
2. `python parseSongid_then_add_everything.py -s/--songid []`可以自动向数据库添加一首歌曲,以及歌曲所在的专辑与相关艺人信息,
并保存相关数据在路径`../database_json/`下
3. `python searchPy.py -s/--search []` 可以关键词搜索并保存数据文件


