环境：python3， mysql

主要依赖 django, pymysql

安装依赖 执行 
`pip install -r requirements.txt`

同级目录下放置好脱库数据集data_json/文件夹后，
按照如下顺序依次建表
(注：默认用户名密码数据库名都在connection中写明)


1. _createMusicDatebase.sql
2. createAlbumsTables.py
3. createArtistsTables.py
4. createSongsTables.py
5. createSongArtistAlbumsTables.py
6. create_utils.py


