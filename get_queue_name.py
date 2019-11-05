#!/usr/bin/python2.7
# coding=utf-8
#获取MQ主机消息队列名称列表
import json,requests,sys
#rabbid mq主机
Url="http://172.31.0.53:15672/api/queues/"

user='admin'
password='BHUnjiMKO'

#http get
s=requests.session()
s.auth = (user,password)
try:
    r = s.get(Url,timeout=5)
except requests.exceptions.Timeout :
    print -1
else:
    #json to string
    msg={"data":[]}
    #print r.text
    res=json.loads(r.text)
    #print res[0]["name"],res[0]["messages"]
    for i in range(0,len(res)):
        #print("queue NO."+str(i)+":"+str(res[i]["name"])+":"+str(res[i]["messages"]))
        msg["data"]+=[{"{#NAME}":str(res[i]["name"]),"messages_total":res[i]["messages"],"messages_unacknowledged":res[i]["messages_unacknowledged"]}]
    print json.dumps(msg)
    f=open("/etc/zabbix/script/rabbitmq2/queue_status_prod.txt","w")
    json.dump(msg,f,indent=4)
    f.close()
