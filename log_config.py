import logging

# 创建顶层 Logger
main_logger = logging.getLogger('app')
main_logger.setLevel(logging.DEBUG)

# 创建控制台 Handler 并设置级别
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# 创建文件 Handler 并设置级别
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# 将 Handler 添加到 Logger
main_logger.addHandler(console_handler)
main_logger.addHandler(file_handler)

## 创建子 Logger
#db_logger = logging.getLogger('app.database')
#network_logger = logging.getLogger('app.network')

if __name__ ==  "__main__":
    # 使用 Logger 输出日志
    main_logger.info("This is an info message from the main app")
    #db_logger.debug("This is a debug message from the database module")
    #network_logger.error("This is an error message from the network module")

