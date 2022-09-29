# CGI+WebServer

#### 介绍

    北京理工大学CGI，多线程WebServer作业

#### 文件结构

    webroot 网站根目录
    webroot/src 网络服务器
    webroot/cgi-bin CGI程序
    webroot/css css
    webroot/picture 图片
    webroot/html 静态网页
    webroot/log 日志

#### 环境安装

    在云服务器上装好对应的mysql数据库

    使用pip进行虚拟环境管理，请预装好python 3.8.10 或使用其他包管理器

    git clone https://github.com/zhixiaoni/CGI-WebServer.git

    python -m venv webroot

    webroot/.venv/Scripts/activate

    (.venv) pip install -r webroot/requirements.txt

#### 使用说明

    数据库云服务器ssh连接设置在webroot/cgi-bin/parameter.py，如ip,port, ssh用户和密码

    直接运行即可
    (.venv) python webroot/src/main.py -p xxxx --ip x.x.x.x -maxc x -maxw x

    参数默认值：port 8888, ip 127.0.0.1, maxc最大连接8, maxw 最大等待16

    日志在log目录下