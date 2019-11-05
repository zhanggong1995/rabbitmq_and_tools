#!/usr/bin/python2.7
# coding=utf-8
# 从文件中读取对应队列名称的消息数
# 入参为队列名，返回total_messages数量

import sys,json,fcntl
queue_name=sys.argv[1]
env=sys.argv[2]
key_word="messages_total"
f_name=""
if env=="prod":
    f_name="/etc/zabbix/script/rabbitmq2/queue_status_prod.txt"
elif env=="rabbitmq":
    f_name="/etc/zabbix/script/rabbitmq2/queue_status_rabbitmq.txt"
f=open(f_name,"r")
fcntl.flock(f.fileno(), fcntl.LOCK_EX)
data=f.read()
c=json.loads(data,encoding="utf-8")
for key in c["data"]:
    if key['{#NAME}']==queue_name:
        print key[key_word]
fcntl.flock(f.fileno(), fcntl.LOCK_UN)
f.close()
