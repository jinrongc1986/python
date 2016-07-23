#-*- coding:utf-8 -*- 
import pymysql
import paramiko
import time
from _overlapped import NULL
start2 = time.clock()
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
####读取本地数据库###################
conn=pymysql.connect(host="192.168.1.166",port=3306,user="root",passwd="123456",db="jinrongc",charset="utf8")
cursor =conn.cursor()
sql ="select * from http_cache_info;"
cursor.execute(sql)
row=cursor.fetchall()
####连接到linux进行curl测试###########

ssh.connect('192.168.1.68',port=22,username = 'root',password='123456',timeout=5)
cnt1=0
cnt2=0
cnt3=0
cnt4=0
for r in row:
    a=r[0]
    b=r[1]
    c=r[2]
    cnt4+=1
    CL_flag=0
    curl_uri="curl --head '"+b+"'"
    stdin, stdout, stderr=ssh.exec_command(curl_uri)
    out = stdout.readlines()
######进行curl原始uri,并判断Content-Length有无发生变化####################
######若有变化，则更新到数据库并记录变化值################################
    for CL_str in out:
        if "Content-Length:" in CL_str:
            CL=CL_str.split()[1]
#            print (type(CL))
            CL_flag=1
            if c==None:
                c=CL
                ####把第一次采集的Content-Length数据写入本地mysql###############
                sql =" UPDATE http_cache_info SET ContentLength="+c+" WHERE md5= '"+a+"';"
                cursor.execute(sql)
                cnt1+=1
            elif int(c)==int(CL):
                cnt2+=1
            else:
                cursor.execute("select * from CL_change where md5='%s'"%a)
                recorded=cursor.fetchall()
                if(recorded==()):
                ####若CL发生变化，则在CL_change表生成一条日志并记录相关值##############
                    sql =" insert into CL_change (md5,uri,ContentLength,New_ContentLength,change_stat) values ('"+a+"','"+b+"',%d,%d,1);"%(c,int(CL))
                    cursor.execute(sql)
                cnt3+=1
########debug,查看请求响应无CL的具体内容#############################
'''
    if CL_flag==0:
        print (curl_uri)
        print (out)
        print ("###########################################################")
'''
end2 = time.clock()
cnt5=cnt4-cnt1-cnt2-cnt3
total_time_2=end2-start2
print ("总计有%d条数据，其中%d条数据没有变化,新增%d条数据，有%d条数据发生变化,有%d条没有Content-Length响应，总运行时间时间总计%d秒"%(cnt4,cnt2,cnt1,cnt3,cnt5,total_time_2))
conn.close()
ssh.close()
