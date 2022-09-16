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
parser.add_argument('-p','--port', default = 12141)
# 解析
args = parser.parse_args()
# 参数
ip = args.ip
port = args.port





