#!/usr/bin/python2.7
# coding=utf-8
import commands
import os,time,logging
#定义常量
api_server_path="/home/ec2-user/java/api-server/logs/"
backup_path="/home/ec2-user/java/api-server/logs"
log_path="/var/log/backup_api-server_log.log"

date=time.strftime("%Y-%m-%d")

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

#打包并删除日志
def tar_and_delete_1f(source,dst):
    if not os.path.exists(dst):
        logger.error("ERR:备份路径不存在")
        exit(-1)
    if not os.path.exists(source):
        logger.error("ERR:api-server路径不存在")
        exit(-1)
    os.chdir(source)
    (status, output) = commands.getstatusoutput("ls -lrht |grep '.log$'")
    logger.info(output)
    s = str.split(output, "\n")
    if len(s) <= 1:
        logger.error("检测到日志数量小于2，程序退出")
        exit(-1)
    else:
        str1 = str.split(s[-2])
        logger.info("开始压缩："+str1[-1])
        (status, output) = commands.getstatusoutput(
            "tar -czf " + backup_path+"/"+str1[-1] +".tar.gz "+str1[-1]+" --remove-files"
        )
        if status!=0:
            logger.error("压缩出错，错误码："+status)
            logger.error(" "+status)
            return -1
        else:
            logger.info("压缩成功")
            return 0
#只保留3天内的日志备份
def delete_old_tar(tar_path):
    os.chdir(tar_path)
    (status,output)=commands.getstatusoutput('find . -mtime +3 -name "*.tar.gz" -print -exec rm -rf {} \;')
    if status!=0:
        logger.error("find执行失败，返回值："+status)
        return -1
    else:
        logger.info("成功删除旧日志备份：")
        logger.info(output)
        return 0


if __name__=="__main__":
    logger.info("--------------------------------")
    logger.info("日志备份开始执行，路径检查：")
    logger.info("    api-server日志路径："+api_server_path)
    logger.info("    备份路径："+backup_path)

    if 0==tar_and_delete_1f(api_server_path, backup_path):
        logger.info("打包备份成功，开始删除老旧备份")
    if 0==delete_old_tar(backup_path):
        logger.info("成功！！")
