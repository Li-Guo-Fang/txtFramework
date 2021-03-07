
import requests
import json
import os
import hashlib
import random
import re
from server_info import *


'''
创建uniquenumber.txt文件存储数字，然后每次读取uniquenumber里面的数字，
使用后将数字+1再写回去，可保证数字完全不会重复使用
'''



def get_uniquenumber():
    '''读取文件中的数字，用于合成一个唯一的用户名'''
    with open("uniquenumber", "r+", encoding="utf-8") as fp:
        uniquenumber = int(fp.read().strip())
        fp.seek(0, 0)
        fp.write(str(uniquenumber + 1))
    return str(uniquenumber)

def md5(data):
    '''MD5加密数据'''
    m5 = hashlib.md5()
    m5.update(data.encode("utf-8"))
    md5_data = m5.hexdigest() # 16进制32位长度
    return md5_data

def send_request(url, data):
    '''请求接口，获取返回数据'''
    print("request data: %s" % data)
    if isinstance(data, dict):
        data = json.dumps(data) # 数据转换为json传
    response = requests.post(url, data)
    return response


def assert_result(response, key_word):
    '''对结果进行断言'''
    try:
        assert key_word in response.text
        print("断言成功")
        return True
    except AssertionError as e:
        print("断言失败")
        return False
    except:
        print('未知异常')
        return False

