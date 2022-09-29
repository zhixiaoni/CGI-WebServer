from sshtunnel import SSHTunnelForwarder
import pymysql

import cgi

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

# 执行sql语句
cur.execute("""SELECT * from DISHES""")
data = cur.fetchall()

# 打印html页面
print('''
	<html>
    <head>
        <meta charset="utf-8">
        <title>Delete dishes</title>
        <link rel="stylesheet" href="../css/demo.css">
        <script type="text/javascript" src="../js/demo.js"></script>
    </head>
    <body background="../picture/dynamic/background.jpg" style="background-attachment:fixed;background-size:100%;">
        
        <fieldset style="width: 40rem;height: 97%;margin:0 auto;border-radius: 0.5rem;background-color: rgba(240, 248, 255, 0.622);">
		
            <fieldset style="width: 30rem;height: 5%;margin:0 auto;border:none;font-size: xx-large;text-align: center;text-decoration: dashed;-webkit-text-stroke: 0.5px rgb(254, 254, 254);font-weight: 900;">
                Delete dishes
            </fieldset> 
            <div style="width:100%;;border-bottom:3px solid #000000;"></div>
            <form name="dishes" action="/cgi-bin/delete_dishes.py" method="post" target="_blank">
            <fieldset style="border: none; height:78%;overflow-y: scroll;">
''')

# 打印数据
print('''<h3>Please tick √ in the □ about the dishes you need to delete:</h3>''')
for item in data:
    print('''<fieldset style="border-radius: 0.5rem;"><div style = "font-weight: 700;">''', end="")
    print(item[1], end="")
    print('''</div> <div>''', end="")
    print(item[2], end="")
    print('''</div>￥''', end="")
    print(item[3], end="")
    print('''<label><input name="del_dishes" type="checkbox" value="''')
    print(item[0], end="")
    print('''"</label></fieldset>''')

print('''</fieldset>
            <div style="width:100%;height: 1rem;border-top:3px solid #000000;"></div>
                <input  class="button button2" style="margin:0 auto;" type="submit" value="Confirm the deletion" /></form>
        </fieldset><div style="width:100%;height: 1rem;border:none;"></div>
    </body>
</html>''', end="")

# 游标、连接关闭
cur.close()
con.close()
# 云服务器关闭
server.close()
