#-*- coding:utf-8 -*-
import pymysql
import time
start1=time.clock()
conn=pymysql.connect(host="192.168.1.68",port=3306,user="root",passwd="0rd1230ac",db="unknown",charset="utf8")
cursor = conn.cursor()
sql1="select host,count(*),sum(service_size)/sum(cache_size),sum(cache_size),sum(cache_time),sum(service_size),sum(service_time) from video_cache GROUP BY host;"
cursor.execute(sql1)
hostgroup=cursor.fetchall()
cnt_1=0
for row in hostgroup:
    if row[1]>100:
        print (row)
        cnt_1+=1
        cursor.execute("select * from video_cache_sum where host='%s'"%row[0])
        recorded=cursor.fetchall()
        if(recorded==()):
        ####若此host不存在在数据表中，则在CL_change表生成一条日志并记录相关值##############
            sql =" insert into video_cache_sum (host,cnt,ratio,cache_size,cache_time,service_size,service_time) values ('%s',%d,,%f,%d,%d,%d,%d);"%(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
            print (sql)
            cursor.execute(sql)
        else:
            sql =" update video_cache_sum set host='%s',cnt=%d,ratio=%f,cache_size=%d,cache_time=%d,service_size=%d,service_time=%d where host='%s';"%(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[0])
            print (sql)
            cursor.execute(sql)
conn.close()
end1=time.clock()
total_time=end1-start1
print (("总计花费%.2f秒时间,总共有%d个host热点（点击数超过100）")%(total_time,cnt_1))