import os
import argparse

# path
# dir
webroot_path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
src_path = os.path.abspath(os.path.dirname(__file__))
CGI_WebServer_path = os.path.abspath(os.path.join(webroot_path,".."))
log_path = os.path.join(webroot_path,r"log")
html_path = os.path.join(webroot_path,r"html")
CGI_path = os.path.join(webroot_path,r"cgi-bin")
picture_path = os.path.join(webroot_path,r"picture")

#file
index_path = os.path.join(webroot_path,r"index.html")
html404_path = os.path.join(webroot_path,r"404.html")
html400_path = os.path.join(html_path,r"400.html")
html403_path = os.path.join(html_path,r"403.html")
admin_path = os.path.join(webroot_path,r"admin.html")
student_path =  os.path.join(webroot_path,r"student.html")
# net
# 参数解析器
parser = argparse.ArgumentParser()
# 添加参数
parser.add_argument('--ip', default = "127.0.0.1")
parser.add_argument('-p', '--port', default = 8888)
parser.add_argument('-maxc', '--maxConnection', default= 8)
parser.add_argument('-maxw', '--maxWaiting', default= 16)
# 解析
args = parser.parse_args()
# 参数
ip = args.ip
port = int(args.port)
maxConnection = int(args.maxConnection)
maxWaiting = int(args.maxWaiting)




