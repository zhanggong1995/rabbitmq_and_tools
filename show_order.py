#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-
import re,os,time,datetime
#vars:
order_path="info.log"
rows=11


#defines:
def print_with_color(num, a, b):
    #控制输出的颜色
    errlist=[1,3,4,5,10]
    if a==0 or b==0:
        print '<font color=#FFFFFF size="3" ><strong>'
        print num[a][b]
        print '</strong></font>'
        return
    if b in errlist and num[a][b]!='0':
    #if b==10 and num[a][b]!='0':
        print '<font color=#FF0000 >'
        print num[a][b]
        print ' </font>'
        return
    print '<font color=#00DB00 >'
    print num[a][b]
    print ' </font>'
    return
def print_http_head():
    #输出http头部
    print "Content-type:text/html"
    print  # 空行，告诉服务器结束头部
    print '<html>'
    print '<head >'
    print '<meta charset="utf-8" http-equiv="refresh" content="10" >'
    print '<title>下单状态</title>'
    print '</head>'
    print
    print '<body bgcolor=#000000 >'
def print_time_now():
    current_time = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    print "<font color=#00DB00 >刷新时间:     "+current_time+'  </font></br>'
    print "<font color=#00DB00 >当前时间:</font>"
    print "<font color=#00DB00 >当前时间:</font>"
    #打印现在的时间
    print '<font color=#00DB00 ><span id="cg"> </span> <script> '
    print 'setInterval("cg.innerHTML=new Date().toLocaleString()",1000);'
    print '</script></font >'
def print_http_end():
    #http尾部
    print '</body>'
    print '</html>'
def print_table(arr, l, r):
    #输出表格
    print '<table border="8" cellpadding="10">'
    for a in range(r):
        print '<tr>'
        for b in range(l):
            print '<td align="right">'
            print_with_color(arr, a, b)
            print '</td>'
        print '<tr>'
    print '</table>'
def get_file_lines(f_path):
    if os.path.exists(f_path):
        f=open(f_path,"r")
        count=0
        while True:
            line = f.readline()
            # print text_line
            if line:
                if line == "\n":
                    break
                if re.match("^[a-z]", line, re.I):
                    count += 1
            else:
                break
        f.seek(0)
        #除字母开头交易所外还有汉字开头的表头
        count+=1
        return f,count
    else:
        return 0,0

#main:
if __name__=="__main__":
   #初始化二维数组
    order_file,lines=get_file_lines(order_path)
    array = [[0] * rows for i in range(lines)]
################打印表格
    print_http_head()
    i,j=0,0
    while  i<lines:
        text_line = order_file.readline()
        this_line = text_line.split()
        for j in range(rows):
            array[i][j]=this_line[j]
        i+=1
    order_file.close()
    print_time_now()
    print_table(array, rows, lines)
    print_http_end()
#################
