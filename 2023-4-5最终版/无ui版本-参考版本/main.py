import pickle
from time import sleep
import time
from xml.etree.ElementInclude import include
import requests
import json
# 弹窗模块
import tan
# 使用pathlib检测文件是否存在
from pathlib import Path
# 运行cmd
import subprocess

# 判断文件是否存在（是否初次使用）
if Path("../config.pkl").exists():
    # 读取
    f_read = open('../config.pkl', 'rb')
    conf = pickle.load(f_read)
    print("文件读取：" + str(conf))
    f_read.close()
else:
    tan.chuang("错误：", "找不到配置文件！", 3)
    exit

# 校园网wifi名称
WALN_NAME = "NSU-SDN"
# 账号信息（学号，加密方法（密码））
global username
username = conf["zh"]
global password
password = conf["mm"]
# 获取登陆状态
global getdata
getdata = conf["gd"]
# 登录
global login
login = conf["lo"]
# 获取信息
global getinfo
getinfo = conf["gi"]
# 上线套餐
global sangxian
sangxian = conf["sx"]

# 判断网络情况
def Network():
    cmd_string = "ipconfig"
    re = str(subprocess.Popen(cmd_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='gbk').communicate()[0])
    res = re.split('\n')
    # 状态标志
    EADP = True
    WLAN = True
    for i in range(len(res)):
        item = res[i]
        if "以太网适配器 以太网" in item:
            i += 2
            NextItem = res[i]
            while(NextItem):
                if "媒体已断开连接" in NextItem:
                    EADP = False
                    break
                i += 1
                NextItem = res[i]

        if "无线局域网适配器 WLAN" in item:
            i += 2
            NextItem = res[i]
            while(NextItem):
                if "媒体已断开连接" in NextItem:
                    WLAN = False
                    break
                i += 1
                NextItem = res[i]
    # print("以太网适配器 以太网:%s"%(EADP))
    # print("\n无线局域网适配器 WLAN:%s"%(WLAN))
    if EADP:
        return True
    elif WLAN:
        return True
    else:
        # 扫描wifi
        cmd_string ="netsh wlan show networks"
        re = str(subprocess.Popen(cmd_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='gbk').communicate()[0]).split('\n')
        for item in re:
            if WALN_NAME in item:
                # 连接wifi
                cmd_string = "netsh wlan connect name=" + WALN_NAME
                re = str(subprocess.Popen(cmd_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='gbk').communicate()[0])
                if "已成功完成连接请求" in re:
                    print("已自动连接wifi" + WALN_NAME)
                    return True
                else:
                    return False
            elif "无线局域网接口电源关闭，它不支持请求的操作" in item:
                tan.chuang("自动登录失败：", "wifi开关未打开/找不到校园网\nSSID=" + WALN_NAME, 2)
                print("wifi开关未打开")
                return False
    

# 发送请求的函数
def sendjson(body):
    # 设置请求url
    url = 'http://1.1.1.1/Auth.ashx'
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
def main():
    
    # 检测并尝试连接网络
    if Network():

        # 获取登陆状态
        result = sendjson(getdata)

        if(result["state"] == 'needLogin'):
            # 登录
            lResult = sendjson(login)
            print('Request login: %s' % (lResult["message"]))
            # 获取信息
            IResult = sendjson(getinfo)
            tc = str(IResult["TC"])
            news = "IP:"+IResult["IP"]+"\n姓名:" + IResult["XM"] + \
                "\n用户组:"+IResult["UG"]+"\n套餐:"+tc
            print('get info: %s' % (IResult["state"]))
            # 请求上线
            UpLine = sendjson(sangxian)
            print('up line: %s' % (UpLine["state"]))

            t1 = tan.chuang("登陆："+lResult["message"]+"\n请求上线【" + tc + "】套餐", news,
                            2 if UpLine["state"] != "True" else 1)
        else:
            # python三元运算符不一样
            # 获取信息
            IResult = sendjson(getinfo)
            tc = str(IResult["TC"])
            # 请求上线
            UpLine = sendjson(sangxian)
            t1 = tan.chuang("当前已经登录，请求上线【" + tc + "】套餐:", UpLine["message"],
                            2 if UpLine["state"] != "True" else 1)
            print('up line: %s' % (UpLine["state"]))

        tan.dels(t1)

    else:
        exit


# 初次加载
main()