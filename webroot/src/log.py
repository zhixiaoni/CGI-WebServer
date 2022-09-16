#日志
import os
import parameter
from loguru import logger


#一点示例
#logger.add(sink = os.path.join(parameter.log_path, '1.log'), encoding = 'utf-8',)
#logger.debug("debug")
#logger.info("输出信息")
#logger.warning("警告信息")
#logger.error("错误信息")
