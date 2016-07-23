#-*- coding:utf-8 -*- 
import pymysql
import paramiko
import time
start1=time.clock()
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
####读取现网设备数据##################
conn=pymysql.connect(host="192.168.1.68",port=3306,user="root",passwd="0rd1230ac",db="cache",charset="utf8")
cursor =conn.cursor()
sql ="select * from http_cache where filename rlike '.exe';"
cursor.execute(sql)
row=cursor.fetchall()
conn.close()
####把数据写入本地mysql###############
conn=pymysql.connect(host="192.168.1.166",port=3306,user="root",passwd="123456",db="jinrongc",charset="utf8")
cursor =conn.cursor()
lib_a={}
cnt_1=0
cnt_2=0
for r in row:
    a=r[0]
    b=r[7]
    lib_a[a]=b
    print (a)
    print (b)
    cnt_1+=1
    cursor.execute("select * from http_cache_info where md5='%s'"%a)
    recorded=cursor.fetchall()
    if(recorded==()):
        cnt_2+=1
        sql =" insert into http_cache_info (md5,uri) values ('"+a+"','"+b+"');"
        cursor.execute(sql)
#    for s in r:
#        print (s)
#    print (r.split(','))
conn.close()
end1=time.clock()
total_time_1=end1-start1
print ("总计有%d条记录，新增%d多少条记录，总计花费%d秒。"%(cnt_1,cnt_2,total_time_1))
'''

ssh.connect('192.168.1.68',port=22,username = 'root',password='123456',timeout=5)
m="curl --head "
for key in lib_a:
    n=m+lib_a[key]
    stdin, stdout, stderr = ssh.exec_command(n)
    out = stdout.readlines()
    #屏幕输出
    for o in out:
        if "Content-Length:" in o:
            print(o)


ssh.close()
'''