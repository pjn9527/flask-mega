import requests
from flask import current_app
from app import app
import random 
from hashlib import md5

def translate(text, source_language, dest_language):
    # 安全获取应用上下文
    app = current_app
    
    # 语言代码映射表（标准代码 -> 百度API代码）
    LANGUAGE_MAPPING = {
        # 常用语言
        'zh': 'zh',    # 中文
        'en': 'en',    # 英语
        'es': 'spa',   # 西班牙语
        'fr': 'fra',   # 法语
        'de': 'de',    # 德语
        'ar': 'ara',  # 阿拉伯语（标准: ar -> 百度: ara）
        'ja': 'jp',    # 日语（标准: ja -> 百度: jp）
        'ko': 'kor',   # 韩语
        'ru': 'ru',    # 俄语
        'pt': 'pt',    # 葡萄牙语
        'it': 'it',    # 意大利语
    }

    # 转换语言代码
    source_language = LANGUAGE_MAPPING.get(source_language, source_language)
    dest_language = LANGUAGE_MAPPING.get(dest_language, dest_language)

    # 1. 配置检查
    if not app.config.get('BAIDU_APPID') or not app.config.get('BAIDU_APPKEY'):
        return "翻译服务未配置"
    
    # 2. 参数准备
    appid =app.config['BAIDU_APPID']
    appkey = app.config['BAIDU_APPKEY']
    salt = str(random.randint(10000,99999))
    sign_str = appid + text + salt + appkey

    # 3. 签名生成
    sign = md5(sign_str.encode('utf-8')).hexdigest()

    # 4. 构建请求参数
    params = {
        'q': text,
        'from': source_language,
        'to': dest_language,
        'appid': appid,
        'salt': salt,
        'sign': sign,
        'needIntervene': 0,  # 可选术语库干预
    }

    # 5. 发送API请求
    try:
        r = requests.get(
            'https://fanyi-api.baidu.com/api/trans/vip/translate',
            params=params,
            timeout=5
        )
        r.raise_for_status()    # 检查HTTP状态码
        # 6. 响应处理
        result = r.json()
        if 'error_code' in result:
            return f"翻译错误: {result['error_msg']} (代码: {result['error_code']})"
        
    except requests.exceptions.RequestException as e:  # 捕获异常变量
        return f"翻译服务不可用: {str(e)}"
    except Exception as e:  # 增加通用异常处理
        return f"意外错误: {str(e)}"
    
    
    # 7. 结果提取
    return result['trans_result'][0]['dst']
