from time import sleep
import time
from xml.etree.ElementInclude import include
import requests
import json
# 弹窗模块
import tan

# 账号信息（学号，MD5（密码））
username = '21066666666'
password = '920aa8eb3b98f3ac5fbae141f3bb8150'
# 检测时间间隔（以分钟计算）
Jtime = 30
# 获取登陆状态
getdata = {"DoWhat": "Check"}
# 登录
login = {"username": "%s" % (username), "password": "%s" % (password),
         "remember": "true", "DoWhat": "Login"}
# 获取信息
getinfo = {"DoWhat": "GetInfo"}
# 上线套餐
sangxian = {"DoWhat": "OpenNet", "Package": "学生-移动-100M"}
# 发送请求的函数


def sendjson(body):
    # 设置请求url
    url = 'http://1.1.1.1/Auth.ashx'
    # 设置请求json
    #body = {"DoWhat": "Check"}
    # 序列化成json字符串
    data = json.dumps(body)
    # 设置请求头
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44',
        'Referer': 'http://1.1.1.1/',
        'Cookie': 'username={a}; password={b}'.format(a=username, b=password)
    }
    # 执行post请求
    response = requests.post(url, data=data, headers=headers)
    # 以utf-8的编码解码
    response.encoding = 'utf-8'
    # python的print必须加括号
    # requests库中，不用json.loads方法进行反序列化
    Json = response.json()
    # 创建一个字典(类似数组)
    result = dict()
    # （公共属性）str函数转为字符串
    result["state"] = str(Json.get('Result'))
    result["message"] = str(Json.get('Message'))
    # 判断返回状态(switch)
    if(str(Json.get("DoWhat")) == "GetInfo"):
        # IP
        result["IP"] = str(Json.get('Data').get("IP"))
        # 姓名
        result["XM"] = str(Json.get('Data').get("XM"))
        # 用户组（usergroup）
        result["UG"] = str(Json.get('Data').get("UG"))
        # 套餐名
        result["TC"] = str(Json.get('Data').get("KXTC")[0].get("套餐名称"))
    return result

# 主要的操作函数


def weblogin():
    # 获取登陆状态
    result = sendjson(getdata)

    if(result["state"] == 'needLogin'):
        # 登录
        lResult = sendjson(login)
        t1 = tan.chuangs("当前暂未登录,自动登录结果：", lResult["message"],
                         2 if result["state"] != "True" else 1, t)
        print('Request login: %s' % (lResult["message"]))
        # 获取信息
        IResult = sendjson(getinfo)
        tc = str(IResult["TC"])
        news = "IP:"+IResult["IP"]+"\n姓名:" + IResult["XM"] + \
            "\n用户组:"+IResult["UG"]+"\n套餐:"+tc
        t2 = tan.chuangs("登陆成功，当前账号信息：", news,
                         2 if IResult["state"] != "True" else 1, t1)
        print('get info: %s' % (IResult["state"]))
        # 请求上线
        line = {"DoWhat": "OpenNet", "Package": tc}
        UpLine = sendjson(line)
        t3 = tan.chuangs("请求上线【" + tc + "】套餐:", UpLine["message"],
                         2 if UpLine["state"] != "True" else 1, t2)
        print('up line: %s' % (UpLine["state"]))
        tan.dels(t3)
    else:
        # python三元运算符不一样
        t2 = tan.chuangs("当前已经登录：", result["message"],
                         2 if result["state"] != "True" else 1, t)
        print('The current landing status is: %s' % (result["state"]))


# 初次加载
t = tan.chuangs("欢迎使用-繁寂自登录脚本：", "当前检测时间：【" +
                str(Jtime) + "】(分钟)", 4, tan.new())
time.sleep(3)
weblogin()
# 死循环检测定时
""" while True:
    time.sleep(Jtime * 60)
    weblogin()
 """
