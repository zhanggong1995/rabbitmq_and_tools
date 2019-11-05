#!/usr/bin/python2.7
# coding=utf-8
import commands
import os,time,logging
#定义常量
tomcat_path="/home/ec2-user/boms/tomcat-service/logs"
backup_path="/home/ec2-user/logsback/pre_tomcat"
log_path="/var/log/backup_tomcat_log.log"
stop_tomcat_script = "/home/zhanggong/kill_process.py tomcat-service/"
start_tomcat_script="/home/ec2-user/boms/tomcat-service/bin/startup.sh"

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

#重启tomcat函数
def restart_tomcat():
    #stop_sh="/home/ec2-user/boms/tomcat-service/bin/shutdown.sh"
    stop_sh=stop_tomcat_script
    start_sh=start_tomcat_script
    (status, output) = commands.getstatusoutput(stop_sh)
    if status!=0:
        logger.error("ERR:stop脚本执行失败，返回值："+str(status))
        logger.error(output)
        return -1
    else:
        logger.info("tomcat 已停止,等待执行start脚本...")
        time.sleep(5)
        (status, output) = commands.getstatusoutput(start_sh)
        if status != 0:
            logger.error("start脚本执行失败，返回值：" + str(status)+"请手动开启tomcat")
            logger.error(output)
            return -1
        else:
            logger.info ("tomcat 重启成功！")
            return 0
#打包并删除日志
def tar_and_delete(source,dst):
    if not os.path.exists(dst):
        logger.error("ERR:备份路径不存在")
        exit(-1)
    if not os.path.exists(source):
        logger.error("ERR:tomcat路径不存在！")
        exit(-1)
    os.chdir(source)
    logger.info("切换目录:"+source)
    arg1 = dst + "/tomcat_app-log-" + date + ".tar.gz "
    arg2 = " * "
    logger.info("执行：tar -czf " + arg1 + arg2 + " --warning=no-file-changed")
    (status, output) = commands.getstatusoutput("tar -czf " + arg1 + arg2)
    if status != 0 and status != 256:
        logger.error("ERR:打包失败,返回值：" + str(status))
        logger.error(output)
        return -1
    else:
        logger.info("打包成功!")
        logger.info(output)
        if source.isspace():
            logger.error("警告！检测到空路径！:"+output)
            return -1
        re = os.system("rm -rf " + source + "/*")
        if re == 0:
            logger.info ("已删除" + source + "路径下所有文件")
            return 0
        else:
            logger.error ("ERR:删除失败:" + str(re) + "，请手动删除" + source)
            return -1
#判断tomcat端口是否正常工作
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
    logger.info ("----------------------------------------")
    logger.info ("日志备份开始执行，路径检查：")
    logger.info ("    tomcat日志路径："+tomcat_path)
    logger.info ("    备份路径："+backup_path)

    if 0!=tar_and_delete(tomcat_path,backup_path):
        exit(-1)
    if restart_tomcat()!=0:
        logger.error("tomcat重启出错，程序执行失败！")
        exit(-1)
    else:
        logger.info("删除旧日志：")
        if 0==delete_old_tar(backup_path):
            logger.info("成功！！")
        else:
            logger.error("删除日志失败，请手动检查")
