from sshtunnel import SSHTunnelForwarder
import pymysql

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
# 执行sql语句
cur.execute("""SELECT * from DISHES""")
# 读取数据
data = cur.fetchall()

# 打印html页面
print('''
	<html>
    <head>
        <meta charset="gb2312">
        <title>查看菜单</title>
        <link rel="stylesheet" href="../css/demo.css">
        <script type="text/javascript" src="../js/demo.js"></script>
    </head>
    <body background="../pictures/background.jpg" style="background-attachment:fixed;background-size:100%;">
        
        <fieldset style="width: 40rem;height: 97%;margin:0 auto;border-radius: 0.5rem;background-color: rgba(240, 248, 255, 0.622);">
		
            <fieldset style="width: 30rem;height: 5%;margin:0 auto;border:none;font-size: xx-large;text-align: center;text-decoration: dashed;-webkit-text-stroke: 0.5px rgb(254, 254, 254);font-weight: 900;">
                查看菜单
            </fieldset> 
            <div style="width:100%;;border-bottom:3px solid #000000;"></div>
            <fieldset style="border: none; height:78%;overflow-y: scroll;">
''')

for item in data:
    print('''<fieldset style="border-radius: 0.5rem;"> <div style = "font-weight: 700;">''', end="")
    print(item[1], end="")
    print('''</div> <div>''', end="")
    print(item[2], end="")
    print('''</div>￥''', end="")
    print(item[3], end="")
    print('''</fieldset>''')

print('''</fieldset></center></form></fieldset><div style="width:100%;height: 1rem;border:none;"></div>
    </body>
</html>''', end="")

# 游标、连接关闭
cur.close()
con.close()
# 云服务器关闭
server.close()