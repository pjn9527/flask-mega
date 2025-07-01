import requests
import random
from hashlib import md5
from flask import current_app

LANGUAGE_MAP = {
    'zh': 'zh', 'en': 'en', 'es': 'spa', 'fr': 'fra', 
    'de': 'de', 'ar': 'ara', 'ja': 'jp', 'ko': 'kor',
    'ru': 'ru', 'pt': 'pt', 'it': 'it'
}

def translate(text, source_lang, dest_lang):
    """精简短语翻译核心"""
    app = current_app._get_current_object()
    appid = app.config.get('BAIDU_APPID')
    appkey = app.config.get('BAIDU_APPKEY')
    if not appid or not appkey:
        return "翻译服务未配置"
    
    # 短语智能检测（3词以内视为短语）
    is_phrase = len(text.split()) <= 3
    
    # 核心参数设置
    params = {
        'q': text,
        'from': 'auto' if is_phrase else LANGUAGE_MAP.get(source_lang, source_lang),
        'to': LANGUAGE_MAP.get(dest_lang, dest_lang),
        'appid': appid,
        'salt': str(random.randint(10000, 99999)),
        'sign': ''
    }
    
    # 动态签名生成（使用原始文本）
    sign_str = f"{appid}{text}{params['salt']}{appkey}"
    params['sign'] = md5(sign_str.encode()).hexdigest()
    
    # 统一请求方法（GET/POST自适应）
    method = requests.get if len(text) < 100 else requests.post
    
    try:
        response = method(
            'https://fanyi-api.baidu.com/api/trans/vip/translate',
            params=params if method == requests.get else None,
            data=params if method == requests.post else None,
            timeout=3
        )
        response.raise_for_status()
        result = response.json()
        
        # 短语错误自动修复
        if 'error_code' in result and result['error_code'] == '58001' and is_phrase:
            params['from'] = 'en'  # 英语作为默认重试语言
            sign_str = f"{appid}{text}{params['salt']}{appkey}"
            params['sign'] = md5(sign_str.encode()).hexdigest()
            response = requests.get(
                'https://fanyi-api.baidu.com/api/trans/vip/translate',
                params=params,
                timeout=3
            )
            response.raise_for_status()
            result = response.json()
        
        return result['trans_result'][0]['dst'] if 'trans_result' in result else f"翻译错误: {result.get('error_msg', '未知错误')}"
    
    except requests.RequestException as e:
        return f"网络错误: {str(e)}"
