#日志
import os
import parameter
from loguru import logger
import time

#一点示例

#logger.debug("debug")
#logger.info("输出信息")
#logger.warning("警告信息")
#logger.error("错误信息")

class MyLog():
    def __init__(self):
        #生成日志在log文件夹下，文件名带时间， 保留七天
        logger.add(sink = os.path.join(parameter.log_path, 'runtime_{time}.log'), encoding = 'utf-8', retention = '7 days')
        
    def LogInfo(self, info):
        logger.info(info)

    def LogDebug(self, info):
        logger.debug(info)
        
    def LogWarning(self, info):
        logger.warning(info)   

    def LogError(self, info):
        logger.error(info)     
    
    def StdInfo(self, ip, request, status, length, userAgent):
        now = time.localtime()
        now_time = time.strftime(r"%d/%B/%Y %H:%M:%S", now)
        return '%s--[%s] %s %d %d %s' % (ip, now_time, request, status, length, userAgent)
        






      

