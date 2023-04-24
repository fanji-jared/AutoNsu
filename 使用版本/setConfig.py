import pickle
import pyDes
# 账号信息（学号，密码原文, 登录套餐名字）
username = '21066666666'
password = '920aa8eb3b98f3ac5fbae141f3bb8150'
taocan = '学生-移动-100M'

# 加密函数
def DES_encrypt_PKCS7(username, password):
    def toHex(txt):
        return ''.join(["%02x" % x for x in txt]).strip()

    key = (username[len(username) - 4:] + username + "12345678")

    # 密钥（pyDes只有PKCS#5(8字节)，PKCS#7需要16字节）（长了可以截取成8位，不够添\0），加密方式，偏移量（ECB不需要填写），填充方式（只有PAD_PKCS5）
    des = pyDes.des(key[0: 8], mode = pyDes.ECB, padmode = pyDes.PAD_PKCS5)

    result = des.encrypt(password)

    return toHex(result)

# 密码密文
password = DES_encrypt_PKCS7(username, password)

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
