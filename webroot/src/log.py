#日志
import os
import parameter
from loguru import logger

#生成日志在log文件夹下，带时间
logger.add(sink = os.path.join(parameter.log_path, 'runtime_{time}.log'), encoding = 'utf-8')

#一点示例

#logger.debug("debug")
#logger.info("输出信息")
#logger.warning("警告信息")
#logger.error("错误信息")

def LogInfo(info):
    logger.info(info)

