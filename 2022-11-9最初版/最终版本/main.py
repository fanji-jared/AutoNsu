import pickle
import threading
import time
from turtle import clear
import webbrowser
import requests
import json
from time import sleep
from xml.etree.ElementInclude import include
# GUI
import tkinter as tk
# 弹窗模块
import tan
# 使用pathlib检测文件是否存在
from pathlib import Path

# 获取登陆状态
getdata = {"DoWhat": "Check"}
# 获取信息
global getinfo
getinfo = {"DoWhat": "GetInfo"}


def thread_it(func, *args):
    '''将函数打包进线程'''
    # 创建
    x = threading.Thread(target=func, args=args)
    # 守护 !!!
    x.setDaemon(True)
    # 启动
    x.start()
    # 阻塞--卡死界面！
    # x.join()


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
        'User-Agent': 'ua',
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
        d = (Json.get('Data'))
        # IP
        result["IP"] = str(d.get("IP"))
        # MAC
        result["mac"] = str(d.get("mac"))
        # 姓名
        result["XM"] = str(d.get("XM"))
        # 用户组（usergroup）
        result["UG"] = str(d.get("UG"))
        # 套餐名
        result["TC"] = str((d.get("KXTC")[0]).get("套餐名称"))
    return result
# 发送请求的函数


def jc_state(app_state, t):
    if app_state == 0:
        zanH = str(gets("http://app.sczxh.top/AutoNeu/get.php", "zanH"))
        zanP = str(gets("http://app.sczxh.top/AutoNeu/get.php", "zanP"))
        t = tan.chuangs(zanH, zanP, 3, t)
        # 字典保存
        dict = {"zh": zh, "mm": mm, "sj": sj, "gg": gs,
                "userinfo": userinfo, "app_state": 0}
        # 保存为pkl文件
        f_save = open('config.pkl', 'wb')
        pickle.dump(dict, f_save)
        f_save.close()
    else:
        if app_state != 1:
            # 字典保存
            dict = {"zh": zh, "mm": mm, "sj": sj, "gg": gs,
                    "userinfo": userinfo, "app_state": 2}
            # 保存为pkl文件
            f_save = open('config.pkl', 'wb')
            pickle.dump(dict, f_save)
            f_save.close()
            # 请求获取当前软件状态(0->暂停使用，1->正常使用，2->更新)
            update_url = gets(
                "http://app.sczxh.top/AutoNeu/get.php", "update_url")
            # 请求获取更新提示
            vi = gets("http://app.sczxh.top/AutoNeu/get.php", "update_name")
            t = tan.chuangs("！发现船新版本：", str(vi), 3, t)
            # 在浏览器中访问url地址
            print(update_url)
            webbrowser.open(str(update_url))
            time.sleep(3)
        else:
            try:
                # 字典保存
                dict = {"zh": zh, "mm": mm, "sj": sj, "gg": gs,
                        "userinfo": userinfo, "app_state": 1}
                # 保存为pkl文件
                f_save = open('config.pkl', 'wb')
                pickle.dump(dict, f_save)
                f_save.close()
                return False
            except:
                return False
    return True
# 在线检测软件状态(0->暂停使用，1->正常使用，2->更新)


def gets(url, data):
    # 设置请求url
    # 设置请求json
    # 设置请求头
    headers = {
        'Content-Type': 'application/json;charset=utf-8'
    }
    # 执行post请求
    response = requests.post(url, data=data, headers=headers)
    return response.text


def main():
    while True:
        #######################################【开始云控】##############################################
        try:
            # 判断ip封禁和姓名封禁
            # 请求获取封禁ip
            banned_ip = gets(
                "http://app.sczxh.top/AutoNeu/get.php", "banned_ip")
            # 请求获取封禁姓名
            banned_name = gets(
                "http://app.sczxh.top/AutoNeu/get.php", "banned_name")

            userinfo = sendjson(getinfo)

            if str(userinfo["IP"]) in str(banned_ip) or str(userinfo["XM"]) in str(banned_name):
                tan.chuangs("警告：", "你已被加入黑名单！禁止使用！", 2, t)
                print("hei ming dan")
                break
            # 请求获取当前软件状态(0->暂停使用，1->正常使用，2->更新)
            app_state = gets(
                "http://app.sczxh.top/AutoNeu/get.php", "app_state")

        except:
            # 判断文件是否存在（是否初次使用）
            if Path("config.pkl").exists():
                #tan.chuang("检测配置文件：", "成功", 1)
                # 读取
                f_read = open('config.pkl', 'rb')
                conf = pickle.load(f_read)
                print("文件读取：" + str(conf))
                f_read.close()
                # 向输入框插入
                s1.delete(0, tk.END)
                s2.delete(0, tk.END)
                s3.delete(0, tk.END)
                s1.insert(0, conf["zh"])
                s2.insert(0, conf["mm"])
                s3.insert(0, conf["sj"])
                if tg.get("1.0") == "":
                    tg.delete("1.0", tk.END)
                    tg.insert("1.0", conf["gg"])
                app_state = conf["app_state"]
            else:
                #tan.chuang("检测配置文件：", "失败", 2)
                # 向输入框插入【默认值】
                s1.delete(0, tk.END)
                s2.delete(0, tk.END)
                s3.delete(0, tk.END)
                s1.insert(0, "")
                s2.insert(0, "")
                s3.insert(0, "30")
                # 默认可以使用
                app_state = 1
        # 根据状态操作("非"操作在python中为~)
        if thread_it(jc_state, int(app_state), t):
            break
        #######################################【结束云控】##############################################
        # 获取登陆状态
        result = sendjson(getdata)
        if(result["state"] == 'needLogin'):
            # 登录
            lResult = sendjson(login)
            t1 = tan.chuangs("当前暂未登录,自动登录结果：", lResult["message"],
                             1 if result["state"] != "True" else 2, t)
            print('1.Request login: %s' % (lResult["message"]))
            # 获取信息
            IResult = sendjson(getinfo)
            tc = str(IResult["TC"])
            news = "IP:"+IResult["IP"]+"\n姓名:" + IResult["XM"] + \
                "\n用户组:"+IResult["UG"]+"\n套餐:"+tc
            t2 = tan.chuangs("登陆成功，当前账号信息：", news,
                             2 if IResult["state"] != "True" else 1, t1)
            print('2.get info: %s' % (IResult["state"]))
            # 请求上线
            line = {"DoWhat": "OpenNet", "Package": tc}
            UpLine = sendjson(line)
            t3 = tan.chuangs("请求上线【" + tc + "】套餐:", UpLine["message"],
                             2 if UpLine["state"] != "True" else 1, t2)
            print('3.up line: %s' % (UpLine["state"]))
            # 字典保存
            userinfo = sendjson(getinfo)
            dict = {"zh": zh, "mm": mm, "sj": sj, "gg": gs,
                    "userinfo": userinfo, "app_state": app_state}
            # 保存为pkl文件
            f_save = open('config.pkl', 'wb')
            pickle.dump(dict, f_save)
            f_save.close()
        else:
            # python三元运算符不一样
            t2 = tan.chuangs("当前已经登录：", result["message"],
                             2 if result["state"] != "True" else 1, t)
            print('The current landing status is: %s' % (result["state"]))
        time.sleep(Jtime * 60)
        print("--------------------------xia yi ci zhi xing----------------------------")
# 主要的操作函数


#######################################【开始GUI】##############################################
window = tk.Tk()
# 窗口标题
window.title("AutoNsu")
# 窗口大小
window.geometry("400x300")
# 阻止Python GUI的大小调整
window.resizable(0, 0)
# 定义一个lable
ti = tk.Label(window,
              text="AutoNsu(1.0)",    # 标签的文字
              font=('楷体', 20),     # 字体和字体大小
              width=400, height=1  # 标签长宽（以字符长度计算）
              )
ti.pack()
# 定义一个lable
ti = tk.Label(window,
              text="1.账号：",    # 标签的文字
              bg='white',     # 标签背景颜色
              font=('楷体', 12),     # 字体和字体大小
              width=9, height=2  # 标签长宽（以字符长度计算）
              )
ti.place(x=0, y=45)
# 定义一个lable
ti = tk.Label(window,
              text="2.密码：",    # 标签的文字
              bg='white',     # 标签背景颜色
              font=('楷体', 12),     # 字体和字体大小
              width=9, height=2  # 标签长宽（以字符长度计算）
              )
ti.place(x=0, y=90)
# 定义一个lable
ti = tk.Label(window,
              text="  3.检测时间间隔(min)：",    # 标签的文字
              bg='white',     # 标签背景颜色
              font=('楷体', 12),     # 字体和字体大小
              width=20, height=2  # 标签长宽（以字符长度计算）
              )
ti.place(x=0, y=135)
# 定义一个lable
ti = tk.Label(window,
              text="繁寂制作",    # 标签的文字
              bg='white',     # 标签背景颜色
              font=('楷体', 8),     # 字体和字体大小
              width=16, height=1  # 标签长宽（以字符长度计算）
              )
ti.place(x=150, y=280)
# 定义一个输入框entry（账号）
s1 = tk.Entry(window,
              show=None,
              fg='black',
              font=('楷体', 18),
              width=15
              )  # 如果是输入密码，可以写show='*'
s1.place(x=90, y=50)
# 定义一个输入框entry（密码）
s2 = tk.Entry(window,
              show=None,
              fg='black',
              font=('楷体', 18),
              width=15
              )  # 如果是输入密码，可以写show='*'
s2.place(x=90, y=95)
# 定义一个输入框entry（时间间隔）
s3 = tk.Entry(window,
              show=None,
              fg='black',
              font=('楷体', 18),
              width=15
              )  # 如果是输入密码，可以写show='*'
s3.place(x=180, y=140)
# 定义一个文本框Text（显示软件公告~一排50个数字/字母和24个汉字）
tg = tk.Text(window,
             width=49,
             height=6,
             highlightcolor="red",
             bg="white",
             fg="red",
             font=("黑体", 12),
             wrap="char",  # 字数够width后是否换行（char，none，word）
             cursor="arrow",  # 鼠标移动时样式（arrow circle cross plus ...）
             # state=tk.DISABLED,  # 状态 tk.DISABLED 禁止输入
             relief=tk.GROOVE  # 边框样式
             )
tg.place(x=2, y=178)

try:
    # 请求获取公告
    gs = gets("http://app.sczxh.top/AutoNeu/get.php", "gg")
    if "<script>" in gs:
        print("<script> in gs")
    else:
        # 删除之前的内容
        tg.selection_clear()
        # 更新公告ui
        tg.insert(1.0, gs)
    try:
        # 请求获取当前软件状态(0->暂停使用，1->正常使用，2->更新)
        app_state = gets("http://app.sczxh.top/AutoNeu/get.php", "app_state")
    except:
        app_state = 1

    if jc_state(app_state, t):
        exit()
except:
    # 判断文件是否存在（是否初次使用）
    if Path("config.pkl").exists():
        #tan.chuang("检测配置文件：", "成功", 1)
        # 读取
        f_read = open('config.pkl', 'rb')
        conf = pickle.load(f_read)
        print("文件读取：" + str(conf))
        f_read.close()
        # 向输入框插入
        s1.insert(0, conf["zh"])
        s2.insert(0, conf["mm"])
        s3.insert(0, conf["sj"])
        #tg.insert(1.0, conf["gg"])
    else:
        #tan.chuang("检测配置文件：", "失败", 2)
        # 向输入框插入【默认值】
        s1.insert(0, "")
        s2.insert(0, "")
        s3.insert(0, "30")
        tg.insert(1.0, "")


def save():
    # 读取【账号】文本框文字
    global zh
    zh = s1.get()
    # 读取【密码】文本框文字
    global mm
    mm = s2.get()
    # 读取【时间间隔】文本框文字
    global sj
    sj = s3.get()
    # 读取【时间间隔】文本框文字
    global gh
    gh = tg.get(1.0)
    # 账号信息（学号，MD5（密码））
    global username
    #username = '21066666666'
    username = str(zh)
    global password
    #password = '920aa8eb3b98f3ac3fbae141f3bb9159'
    # 创建md5对象
    #m = hashlib.md5()
    # python3 里str默认是unicode
    # m.update(mm.encode(encoding='utf-8'))      m.hexdigest()
    password = str(mm)
    # 检测时间间隔（以分钟计算）
    global Jtime
    #Jtime = 30
    Jtime = float(sj)

    # 登录
    global login
    login = {"username": "%s" % (username), "password": "%s" % (password),
             "remember": "true", "DoWhat": "Login"}
    try:
        def getinfo():
            # 获取用户信息
            global userinfo
            userinfo = sendjson(getinfo)
            # 请求获取当前软件状态(0->暂停使用，1->正常使用，2->更新)
            state = gets("http://app.sczxh.top/AutoNeu/get.php", "app_state")
            # 字典保存
            dict = {"zh": zh, "mm": mm, "sj": sj, "gg": gs,
                    "userinfo": userinfo, "app_state": state}
            # 字典转json
            data = json.dumps(dict)
            # 上传
            print(str(gets("http://app.sczxh.top/AutoNeu/log.php", data)))
            # 保存为pkl文件
            f_save = open('config.pkl', 'wb')
            pickle.dump(dict, f_save)
            f_save.close()
        if "<script>" in gs:
            print("<script> in gs")
        else:
            getinfo()

    except:
        # # 读取
        # f_read = open('config.pkl', 'rb')
        # conf = pickle.load(f_read)
        # print("文件读取：" + str(conf))
        # f_read.close()
        # # 获取用户信息
        # userinfo = conf["userinfo"]
        print("Internet is Notfound,userinfo out of LocationFile")

    # 开启一个新线程（避免ui卡死）->进入主操作函数
    global t
    t = tan.chuangs("欢迎使用-AutoNeu：", "当前检测时间间隔：【" +
                    str(Jtime) + "】(分钟)", 4, tan.new())
    thread_it(main)


# 定义一个按钮，并绑定点击事件
b1 = tk.Button(window,
               text="保存\n运行",
               font=('楷体'),
               bd=4,
               width=9, height=2,
               justify='right',
               command=save
               )
b1.place(x=290, y=60)

# 渲染ui
window.mainloop()
#######################################【GUI结束】##############################################
