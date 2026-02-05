import os
import time
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import urllib.parse

# 配置文件路径
config_file_path = "config.json"

# 获取html中的用户信息
def fetch_and_extract_info(session, domain):
    url = f"{domain}/user"

    # 发起 GET 请求
    response = session.get(url)

    if response.status_code != 200:
        print("用户信息获取失败，页面打开异常.")
        return None

    # 解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到所有 script 标签
    script_tags = soup.find_all('script')

    # 提取 ChatraIntegration 的 script 内容
    chatra_script = None
    for script in script_tags:
        if 'window.ChatraIntegration' in str(script):
            chatra_script = script.string
            break

    if not chatra_script:
        print("未识别到用户信息")
        return None

    # 使用正则表达式提取需要的信息
    user_info = {}
    user_info['expire'] = re.search(r"'Class_Expire': '(.*?)'", chatra_script).group(1) if re.search(r"'Class_Expire': '(.*?)'", chatra_script) else None
    user_info['unused'] = re.search(r"'Unused_Traffic': '(.*?)'", chatra_script).group(1) if re.search(r"'Unused_Traffic': '(.*?)'", chatra_script) else None

    # # 输出用户信息
    # 用户信息 = f"到期时间: {user_info['到期时间']}\n剩余流量: {user_info['剩余流量']}\n"

    # 提取 Clash 订阅链接
    for script in script_tags:
        if 'index.oneclickImport' in str(script) and 'clash' in str(script):
            link = re.search(r"'https://checkhere.top/link/(.*?)\?sub=1'", str(script))
            if link:
                user_info['clash_link'] = f"https://checkhere.top/link/{link.group(1)}?clash=1"
                user_info['v2ray_link'] = f"https://checkhere.top/link/{link.group(1)}?sub=3"
                break
    return user_info

def generate_config():
    # 获取环境变量
    domain = os.getenv('DOMAIN', 'https://69yun69.com')
    bark_key = os.getenv('BARK_KEY')
    bark_server = os.getenv('BARK_SERVER', 'https://api.day.app')

    # 获取用户和密码的环境变量
    accounts = []
    index = 1

    while True:
        user = os.getenv(f'USER{index}')
        password = os.getenv(f'PASS{index}')

        if not user or not password:
            break

        accounts.append({
            'user': user,
            'pass': password
        })
        index += 1

    # 构造配置数据
    config = {
        'domain': domain,
        'BarkKey': bark_key,
        'BarkServer': bark_server,
        'accounts': accounts
    }
    print(config)
    return config

# 发送消息到 Bark 的函数
def send_message(msg="", BarkKey="", BarkServer="https://api.day.app"):
    # 获取当前 UTC 时间，并转换为北京时间（+8小时）
    now = datetime.utcnow()
    beijing_time = now + timedelta(hours=8)
    formatted_time = beijing_time.strftime("%Y-%m-%d %H:%M:%S")

    # 如果配置了 Bark Key，则发送消息
    if BarkKey != '':
        # 构建消息内容
        message_text = f"执行时间: {formatted_time}\n{msg}"

        # 构造 Bark 请求 URL
        url = f"{BarkServer}/{BarkKey}/{urllib.parse.quote('69云签到')}/{urllib.parse.quote(message_text)}"

        try:
            # 发送 GET 请求
            response = requests.get(url, timeout=10)
            return response
        except Exception as e:
            print(f"发送Bark消息时发生错误: {str(e)}")
            return None

# 登录并签到的主要函数
def checkin(account, domain, BarkKey, BarkServer):
    user = account['user']
    pass_ = account['pass']

    checkin_result_message = f"地址: {domain[:9]}****{domain[-5:]}\n账号: {user[:1]}****{user[-5:]}\n密码: {pass_[:1]}****{pass_[-1]}\n\n"

    try:
        # 检查必要的配置参数是否存在
        if not domain or not user or not pass_:
            raise ValueError('必需的配置参数缺失')

        # 创建 Session 对象
        session = requests.Session()

        # 设置通用的请求头
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
        })

        # 登录请求的 URL
        login_url = f"{domain}/auth/login"

        # 登录请求的 Payload（请求体）
        login_data = {
            'email': user,
            'passwd': pass_,
            'remember_me': 'on',
            'code': "",
        }

        # 设置登录请求的特定请求头
        login_headers = {
            'Origin': domain,
            'Referer': f"{domain}/auth/login",
        }

        # 发送登录请求
        login_response = session.post(login_url, json=login_data, headers=login_headers)

        print(f'{user}账号登录状态:', login_response.status_code)

        # 如果响应状态不是200，表示登录失败
        if login_response.status_code != 200:
            raise ValueError(f"登录请求失败: {login_response.text}")

        # 解析登录响应的 JSON 数据
        login_json = login_response.json()

        # 检查登录是否成功
        if login_json.get("ret") != 1:
            raise ValueError(f"登录失败: {login_json.get('msg', '未知错误')}")

        # 等待确保登录状态生效
        time.sleep(1)

        # 签到请求的 URL
        checkin_url = f"{domain}/user/checkin"

        # 设置签到请求的特定请求头
        checkin_headers = {
            'Origin': domain,
            'Referer': f"{domain}/user/panel",
            'X-Requested-With': 'XMLHttpRequest'
        }

        # 发送签到请求（Session 会自动携带 cookies）
        checkin_response = session.post(checkin_url, headers=checkin_headers)

        print(f'{user}账号签到状态:', checkin_response.status_code)

        # 获取签到请求的响应内容
        response_text = checkin_response.text

        try:
            # 尝试解析签到的 JSON 响应
            checkin_result = checkin_response.json()
            账号信息 = f"地址: {domain}\n账号: {user}\n密码: {pass_}\n"

            # 使用 session 获取用户信息
            userinfo = fetch_and_extract_info(session, domain)

            # 根据返回的结果更新签到信息
            if checkin_result.get('ret') == 1 or checkin_result.get('ret') == 0:
                # checkin_result_message = f"🎉 签到结果 🎉\n {checkin_result.get('msg', '签到成功' if checkin_result['ret'] == 1 else '签到失败')}"
                checkin_result_message =checkin_result.get('msg').split('\n')[0] if checkin_result.get('msg') else '签到结果未知'
            else:
                checkin_result_message = '签到结果未知'
        except Exception as e:
            # 如果出现解析错误，检查是否由于登录失效
            if "登录" in response_text:
                raise ValueError('登录状态无效，请检查Cookie处理')
            raise ValueError(f"解析签到响应失败: {str(e)}\n\n原始响应: {response_text}")

        # 发送签到结果到 Bark
        send_message( f'{checkin_result_message}({userinfo['unused']})', BarkKey, BarkServer)

        return checkin_result_message

    except Exception as error:
        # 捕获异常，打印错误并发送错误信息到 Bark
        print(f'{user}账号签到异常:', error)
        checkin_result_message = f"签到过程发生错误: {error}"
        send_message(checkin_result_message, BarkKey, BarkServer)
        return None

# 主程序执行逻辑
if __name__ == "__main__":
    # 读取配置
    config = generate_config()

    # 读取全局配置
    domain = config['domain']
    BarkKey = config['BarkKey']
    BarkServer = config['BarkServer']
    print(config)
    # 循环执行每个账号的签到任务
    for i, account in enumerate(config.get("accounts", [])):
        print("----------------------------------签到信息----------------------------------")
        checkin_result = checkin(account, domain, BarkKey, BarkServer)
        print(checkin_result)
        print("---------------------------------------------------------------------------")
