import os
import argparse

# path
webroot_path = os.path.abspath("..")
src_path = os.getcwd()
CGI_WebServer_path = os.path.abspath(r"../..")
log_path = os.path.join(webroot_path,r"log")

# net
# 参数解析器
parser = argparse.ArgumentParser()
# 添加参数
parser.add_argument('--ip', default = "127.0.0.1")
parser.add_argument('-p', '--port', default = 8888)
parser.add_argument('-maxc', '--MaxConnection', default= 8)
parser.add_argument('-maxw', '--MaxWaiting', default= 16)
# 解析
args = parser.parse_args()
# 参数
ip = args.ip
port = args.port
MaxConnection = args.MaxConnection
MaxWaiting = args.MaxWaiting




