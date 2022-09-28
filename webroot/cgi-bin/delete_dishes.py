from operator import index
from sshtunnel import SSHTunnelForwarder
import pymysql
import execjs


import cgi

header = 'Content-Type: text/html'
 
print(header)
# 通过SSH连接云服务器
server = SSHTunnelForwarder(
	ssh_address_or_host=("152.136.113.252", 12141),  # 云服务器地址IP和端口port
	ssh_username="team",  # 云服务器登录账号admin
	ssh_password="team",  # 云服务器登录密码password
	remote_bind_address=('localhost', 3306)
)

# 云服务器开启
server.start()
# 云服务器上mysql数据库连接
con = pymysql.connect(host='127.0.0.1',
                      port=server.local_bind_port,
                      user="computer_network",
                      password="a_simple_password",
                      db="computer_network",
                      charset='utf8')
# 创建游标
cur = con.cursor()

# 获取数据
form = cgi.FieldStorage()

# 打印html页面
print('''
<html>
    <head>
        <meta charset="gb2312">
        <title>删除结果</title>
        <link rel="stylesheet" href="../css/demo.css">
        <script type="text/javascript" src="../js/demo.js"></script>
    </head>
    <body background="../pictures/background.jpg" style="background-attachment:fixed;background-size:100%;">
        
        <fieldset style="width: 40rem;height: 97%;margin:0 auto;border-radius: 0.5rem;background-color: rgba(240, 248, 255, 0.622);">
		
            <fieldset style="width: 30rem;height: 5%;margin:0 auto;border:none;font-size: xx-large;text-align: center;text-decoration: dashed;-webkit-text-stroke: 0.5px rgb(254, 254, 254);font-weight: 900;">
                删除结果
            </fieldset> 
            <div style="width:100%;;border-bottom:3px solid #000000;"></div>
            <fieldset style="border: none; height:78%;overflow-y: scroll;">
            <h2>删除成功！</h2>
            <br><a href="../index.html"  target="opentype">跳转到主页</a>
            </fieldset>
''')

#print(len(form["del_dishes"]))
for item in form["del_dishes"]:
    sql = "DELETE FROM DISHES WHERE ID=" + item.value
    cur.execute(sql)
    con.commit()

print('''</fieldset>
    </body>
</html>
''')

# 游标、连接关闭
cur.close()
con.close()
# 云服务器关闭
server.close()