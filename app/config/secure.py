"""
configuration file for project(ignored)
"""

DEBUG = True
# DEBUG = False
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Root@localhost:3306/fisher?charset=utf8mb4'
SECRET_KEY = '39DB4091B9A3655E0060584B842D3F6E1FC1F059B1A775739043C194'
RECENT_GIFT_COUNT = 30

# Email配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = '1741824619@qq.com'
MAIL_PASSWORD = 'qmbvnvftnriwdbef'
