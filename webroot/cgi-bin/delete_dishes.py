from sshtunnel import SSHTunnelForwarder
import pymysql
import parameter


import cgi


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

# 打印html页面
print('''
<html>
    <head>
        <meta charset="utf-8">
        <title>Delete results</title>
        <link rel="stylesheet" href="../css/demo.css">
        <script type="text/javascript" src="../js/demo.js"></script>
    </head>
    <body background="../picture/dynamic/background.jpg" style="background-attachment:fixed;background-size:100%;">
        
        <fieldset style="width: 40rem;height: 97%;margin:0 auto;border-radius: 0.5rem;background-color: rgba(240, 248, 255, 0.622);">
		
            <fieldset style="width: 30rem;height: 5%;margin:0 auto;border:none;font-size: xx-large;text-align: center;text-decoration: dashed;-webkit-text-stroke: 0.5px rgb(254, 254, 254);font-weight: 900;">
                Delete results
            </fieldset> 
            <div style="width:100%;;border-bottom:3px solid #000000;"></div>
            <fieldset style="border: none; height:78%;overflow-y: scroll;">
            <h2>Deleted successfully！</h2>
            <br><a href="../index.html"  target="opentype">Jump to Homepage</a>
            </fieldset>
''')
#执行删除
def isiterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False

if(isiterable(form["del_dishes"])):
    for item in form["del_dishes"]:
        sql = "DELETE FROM DISHES WHERE ID=" + item.value
        cur.execute(sql)
        con.commit()
else:
    sql = "DELETE FROM DISHES WHERE ID=" + form["del_dishes"].value
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
