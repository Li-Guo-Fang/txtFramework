#encoding=utf-8

import re
from server_info import *
from util import get_uniquenumber,send_request,md5,assert_result

global_values = {}

def pre_data_handler(data):
    #global global_values
    # 处理读出来的测试数据
    # 处理请求body信息
    if re.search(r"\$\{unique_\w+\}", data):  # 匹配用户名参数
        var_name = re.search(r"\$\{(unique_\w+)\}", data).group(1)
        var_name = var_name.split("_")[1]
        unique_num = get_uniquenumber()  # 获取唯一数
        print("替换前 data:", data)
        data = re.sub(r"\$\{unique_\w+\}", unique_num, data)  # 将参数替换为唯一数
        global_values[var_name] = str(unique_num)
        print("global_values:%s " % global_values)
        print("替换后 data:", data)

    if re.search(r"\$\{(\w+)\}", data):  # 将注册的用户名的唯一数取出用于后续用户名拼接
        replaceVarList = re.findall(r"\$\{(\w+)\}", data)
        print("需要替换的数据: %s" % replaceVarList)
        for var_name in replaceVarList:
            print("替换前 data:", data)
            data = re.sub(r"\$\{%s\}" % var_name, str(global_values[var_name]), data)
            print("替换后 data:", data)

    # 处理函数部分，${fun()}的形式
    if re.search(r"\$\{\w+\(.+\)\}", data):
        var_pwd = re.search(r"\$\{(\w+\(.+\))\}", data).group(1)
        print("var_pwd: %s" % var_pwd)
        print("eval(var_pwd): %s" % eval(var_pwd))
        data = re.sub(r"\$\{\w+\(.+\)\}", eval(var_pwd), data)
        print("data after replace: %s" % data)
    return data

def get_test_data(data_file):
    test_cases = []
    with open(data_file, 'r') as fp:
        for line in fp:
            line = line.strip()
            api_url = eval(line.split("||")[0].strip()) # 获取url
            print("api_url: %s" % api_url)
            test_data = pre_data_handler(line.split("||")[1].strip())
            print("test_data: %s" % test_data)
            assert_key = line.split("||")[2].strip()
            print("assert_key: %s" % assert_key)
            var_regx = line.split("||")[3].strip()
            print("var_regx: %s" % var_regx)
            test_cases.append([api_url, test_data, assert_key,var_regx])
    return test_cases


# 获取关联变量
def test_data_post_hander(data, regx):
    print("response data: %s" % data)
    print("regx: %s" % regx)
    #global global_values
    if regx.lower().find("none") >= 0:
        return
    # token----"token": "(\w+)"
    var_name = regx.split("----")[0]
    print("关联var_name: %s" % var_name)
    regx_exp = regx.split("----")[1]
    print("regx_exp: %s" % regx_exp)
    if re.search(regx_exp, data): # 匹配到正则，就处理关联
        global_values[var_name] = re.search(regx_exp, data).group(1)
        print("关联处理后的global_values： %s" % global_values)
    return

# 处理关联变量
def after_data_handler(data):
    # {"userid":"%{userid}", "token": "%{token}", "title":"python", "content":"python port test"one}
    print("global_values: %s" % global_values)
    # 关联变量替换
    while re.search(r"%{\w+}", data): # 存在需要替换的关联变量
        var_name = re.search(r"%{(\w+)}", data).group(1)
        print("需要替换的变量 ：%s" % var_name)
        print("关联替换前 data: %s" % data)
        # 把data中匹配到的参数用global_vlues[var_name]替换掉，替换次数是1
        data = re.sub(r"%{(\w+)}", global_values[var_name], data,1)
        print("关联替换后data: %s" % data)
    return data



