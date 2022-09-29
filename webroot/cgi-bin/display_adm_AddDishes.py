from sshtunnel import SSHTunnelForwarder
import pymysql


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

# 打印html页面
print('''
	<html>
    <head>
        <meta charset="utf-8">
        <title>Add dishes</title>
        <link rel="stylesheet" href="../css/demo.css">
        <script type="text/javascript" src="../js/demo.js"></script>
    </head>
    <body background="../picture/dynamic/background.jpg" style="background-attachment:fixed;background-size:100%;">
        
        <fieldset style="width: 40rem;height: 97%;margin:0 auto;border-radius: 0.5rem;background-color: rgba(240, 248, 255, 0.622);">
		
            <fieldset style="width: 30rem;height: 5%;margin:0 auto;border:none;font-size: xx-large;text-align: center;text-decoration: dashed;-webkit-text-stroke: 0.5px rgb(254, 254, 254);font-weight: 900;">
                Add dishes
            </fieldset> 
            <div style="width:100%;;border-bottom:3px solid #000000;"></div>
			<form action="/cgi-bin/add_dish.py" method="post" target="_blank">
            <fieldset style="border: none; height:78%;overflow-y: scroll;">
                <p>Please enter the name of the dish: <input type="text" name="name" /></p>
                <p>Please enter the introduction of the dish: </p>
                <p><textarea type="text"  name="describe" cols="80" rows="10"></textarea></p>
                <p>Please enter the price of the dish (Yuan): <input type="text" name="price" /></p>
''')

print('''</fieldset>
            <div style="width:100%;height: 1rem;border-top:3px solid #000000;"></div>
                <input  class="button button2" style="margin:0 auto;" type="submit" value="Confirm the addition" /></center></form>
        </fieldset><div style="width:100%;height: 1rem;border:none;"></div>
    </body>
</html>''', end="")

# 游标、连接关闭
cur.close()
con.close()
# 云服务器关闭
server.close()