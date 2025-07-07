import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'u will never guess'
    SQLALCHEMY_DATABASE_URI = os .environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir,'app.db')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # 开发环境禁用加密
    if os.environ.get('FLASK_ENV') == 'development':
        MAIL_USE_TLS = False
        MAIL_USE_SSL = False
        MAIL_USERNAME = None
        MAIL_PASSWORD = None
    # 生产环境启用加密
    else:
        MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
        MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'false').lower() == 'true'
        MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
        MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # 原始代码，上面是修改过 MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    ADMINS = os.environ.get('ADMINS', '').split(',') if os.environ.get('ADMINS') else []

    POSTS_PER_PAGE = 25
    LANGUAGES = ['en','zh']
    BAIDU_APPKEY = os.environ.get('BAIDU_APPKEY')
    BAIDU_APPID = os.environ.get('BAIDU_APPID')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
