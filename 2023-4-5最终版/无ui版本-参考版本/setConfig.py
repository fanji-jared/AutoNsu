import pickle
# 账号信息（学号，密码密文, 登录套餐名字）
username = '21066666666'
password = '920aa8eb3b98f3ac5fbae141f3bb8150'
taocan = '学生-移动-100M'


# 获取登陆状态
getdata = {"DoWhat": "Check"}
# 登录
login = {"username": "%s" % (username), "password": "%s" % (password),
         "remember": "true", "DoWhat": "Login"}
# 获取信息
getinfo = {"DoWhat": "GetInfo"}
# 上线套餐
sangxian = {"DoWhat": "OpenNet", "Package": "%s" % (taocan)}


# 字典保存
dict = {"zh": username, "mm": password, "gd": getdata,
        "lo": login, "gi": getinfo, "sx": sangxian}
# 保存为pkl文件
f_save = open('../config.pkl', 'wb')
pickle.dump(dict, f_save)
f_save.close()
