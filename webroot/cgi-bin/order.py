from operator import index
from sshtunnel import SSHTunnelForwarder
import pymysql
import parameter
import cgi
import datetime


# 通过SSH连接云服务器
server = SSHTunnelForwarder(
	ssh_address_or_host = parameter.ssh_address_or_host,  # 云服务器地址IP和端口port
	ssh_username = parameter.ssh_username,  # 云服务器登录账号admin
	ssh_password = parameter.ssh_password,  # 云服务器登录密码password
	remote_bind_address= parameter.remote_bind_address
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

# 执行sql语句
cur.execute("""SELECT * from DISHES""")
data = cur.fetchall()

# 打印html页面
print('''
	<html>
    <head>
        <meta charset="utf-8">
        <title>Submit the order</title>
        <link rel="stylesheet" href="../css/demo.css">
        <script type="text/javascript" src="../js/demo.js"></script>
    </head>
    <body background="../picture/dynamic/background.jpg" style="background-attachment:fixed;background-size:100%;">
        
        <fieldset style="width: 40rem;height: 97%;margin:0 auto;border-radius: 0.5rem;background-color: rgba(240, 248, 255, 0.622);">
		
            <fieldset style="width: 30rem;height: 5%;margin:0 auto;border:none;font-size: xx-large;text-align: center;text-decoration: dashed;-webkit-text-stroke: 0.5px rgb(254, 254, 254);font-weight: 900;">
                Submit the order
            </fieldset> 
            <div style="width:100%;;border-bottom:3px solid #000000;"></div>
            <fieldset style="border: none; height:78%;overflow-y: scroll;">
''')

sum = 0
index = 0
for item in form["num"]:
    sum = float(item.value) * float(data[index][3]) + sum
    index = index + 1
dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

cur.execute("insert into ORDERED(TIME, VALUE) values('%s',%s);" % (dt,sum))
con.commit()
print("<center>Ordered successfully！The total amount is：", sum, "</center>")
print('''<br><center><a href="../index.html"  target="opentype">Jump to Homepage</a></center>
</fieldset>
            <div style="width:100%;height: 1rem;border-top:3px solid #000000;"></div>
        </fieldset><div style="width:100%;height: 1rem;border:none;"></div>
    </body>
    
</html>''', end="")

# 游标、连接关闭
cur.close()
con.close()
# 云服务器关闭
server.close()