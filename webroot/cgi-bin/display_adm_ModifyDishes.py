from sshtunnel import SSHTunnelForwarder
import pymysql
import parameter

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
# 执行sql语句
cur.execute("""SELECT * from DISHES""")
# 读取数据
data = cur.fetchall()

# 打印html页面
print('''
	<html>
    <head>
        <meta charset="utf-8">
        <title>Modify dish information</title>
        <link rel="stylesheet" href="../css/demo.css">
        <script type="text/javascript" src="../js/demo.js"></script>
    </head>
    <body background="../picture/dynamic/background.jpg" style="background-attachment:fixed;background-size:100%;">
        
        <div style = "display: none;margin:0 auto;border-radius: 0.5rem; width: 30rem;height: 80%;
        border: 3px solid rgb(25, 24, 22); background-color: white; z-index:1002;  overflow: auto;background-color: rgba(240, 248, 255, 0.622);" id = "changeblock">
        <center style = "margin:5%;"><button onclick="closewindow()" class = "button button1">Return to the previous page</button></center>
        <form action="/cgi-bin/modify.py" method="post" target="_blank">
        <fieldset style="border-radius: 0.5rem;"><label class="input input1">Num:</label><input readonly="readonly" placeholder="123" type="text" class = "input input1" id="change_id" name="change_id" style = "width:20rem;background-color: rgba(240, 248, 255, 0.622);"></input>
            <br> 
            <br> 
            <label class="input input1">Name:</label><input placeholder="123" type="text" id="change_name" name="change_name" style = "width:20rem;background-color: rgba(240, 248, 255, 0.622);"></input>
            <br> 
            <br> 
            <label class="input input1">Intro:</label><input placeholder="123" type="text" id="change_describe" name="change_describe" style = "width:20rem;background-color: rgba(240, 248, 255, 0.622);"></input> 
            <br>
            <br> 
            <div><div style="float:left"><label class="input">Price:</label> 
            <input type="text" placeholder="123" id="change_price" name="change_price" id="change_price" style = "width:20rem;background-color: rgba(240, 248, 255, 0.622);"></div><div style="float:right;">
            </div>  
        </fieldset>
        <center style = "margin:5%;"><button type="submit" class="button button1"> Submit your changes </button></center></div>
        </form> 
        </div>

        <fieldset id = "distable" style="width: 40rem;height: 97%;margin:0 auto;border-radius: 0.5rem;background-color: rgba(240, 248, 255, 0.622);">
		
            <fieldset style="width: 30rem;height: 5%;margin:0 auto;border:none;font-size: xx-large;text-align: center;text-decoration: dashed;-webkit-text-stroke: 0.5px rgb(254, 254, 254);font-weight: 900;">
                Modify dish information
            </fieldset> 
            <div style="width:100%;;border-bottom:3px solid #000000;"></div>
            <fieldset style="border: none; height:78%;overflow-y: scroll;">
''')

# 打印数据
for item in data:
	print('''<fieldset style="border-radius: 0.5rem;"><div id = "name_''', end="")
	print(item[0], end="")
	print('''" style = "font-weight: 700;">''', end="")
	print(item[1], end="")
	print('''</div> <div id = "describe_''', end="")
	print(item[0], end="")
	print('''">''', end="")
	print(item[2], end="")
	print('''</div> <div><div style = "float:left"><label class="input input1">￥</label> <input type="text" readonly="readonly" name="price_''', end="")
	print(item[0], end="")
	print('''" class="input input1" id = "price_''', end="")
	print(item[0], end="")
	print('''" value = ''', end="")
	print(item[3], end="")
	print('''></div><div style="float:right;">''', end="")
	print('''<button type='button' onclick="change(''', end="")
	print(item[0], end="")
	print(''')" class="button button1"> Modify information </div> </div> </div> </fieldset>''', end="")

print('''</fieldset>
            <div style="width:100%;height: 1rem;border-top:3px solid #000000;"></div>
        </fieldset><div style="width:100%;height: 1rem;border:none;"></div>
    </body>
</html>''', end="")

# 游标、连接关闭
cur.close()
con.close()
# 云服务器关闭
server.close()

