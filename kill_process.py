#!/usr/bin/python2.7
# coding=utf-8
import commands,sys
import logging

#定义常量
log_path="/var/log/kill_process.log"
#值为1时只输出PID，不执行kill
IF_TEST=1
#logging模块初始化
logger = logging.getLogger()
logger.setLevel(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#写入日志
handler_file = logging.FileHandler(log_path)
handler_file.setLevel(logging.DEBUG)
handler_file.setFormatter(formatter)
#标准输出
handler_stdout=logging.StreamHandler()
handler_stdout.setLevel(logging.DEBUG)
handler_stdout.setFormatter(formatter)

logger.addHandler(handler_file)
logger.addHandler(handler_stdout)

#通过传入字符截取进程信息
def grep_process(p_name):
    (status, output) = commands.getstatusoutput(
        "ps -e -o \"pid,cmd\" |grep " + p_name + " |grep -v grep|grep -v \'" + sys.argv[0] + "\'")
    str_pid = str.split(output, "\n")
    if str_pid[0]=='':
        logging.error("没有找到此关键字的程序")
        return -1
    elif len(str_pid)!=1:
        logging.error("获取到的进程pid不唯一,请缩小grep范围")
        logging.info("pid列表：")
        for i in str_pid:
            logging.info("--"+i)
        return -1
    else:
        logging.info("获取到唯一的进程：")
        logging.info(str_pid)
        return str_pid
#通过传入字符获取PID
def get_process_pid(p_name):
    r=grep_process(p_name)
    if r==-1:
        return -1
    str_pid=str.split(r[0])
    logging.info("获取到pid:"+str_pid[0])
    return str_pid[0]
#传入PID，执行kill命令
def kill_process_by_pid(pid):
    if IF_TEST==0:
        (status, output) = commands.getstatusoutput("kill -9 "+pid)
        if status!=0:
            logging.error("kill出错，错误码："+status)
            logging.error("错误信息："+output)
            return -1
        else:
            logging.info("进程已关闭："+pid)
            return 0
    elif IF_TEST==1:
        logging.info("kill -9 "+pid)
        return 0
if __name__ == "__main__":
    if len(sys.argv)!=2:
        logging.error("参数个数不正确，请使用 ./kill_process.py 进程名")
    else:
        logging.info("-----------------------------------------")
        logging.info("关键字:"+sys.argv[1]+" 开始执行:")
        ret=get_process_pid(sys.argv[1])
        if ret==-1:
            logging.error("获取PID失败，程序退出")
            exit(-1)
        else:
            if 0==kill_process_by_pid(ret):
                logging.info("成功!!")
                exit(0)
            else:
                exit(-1)