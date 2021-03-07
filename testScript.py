#encoding=utf-8

import re
import time
from server_info import *
from util import get_uniquenumber,send_request,md5,assert_result
from data_handler import get_test_data, pre_data_handler, test_data_post_hander, after_data_handler
from send_mail import send_mail
from html_report import report_html


'''
创建uniquenumber.txt文件存储数字，然后每次读取uniquenumber里面的数字，
使用后将数字+1再写回去，可保证数字完全不会重复使用
'''

total_test_case = 0 # 总用例数
success_test_case = 0 # 成功用例数
failed_test_case = 0 # 失败用例数

# 读取文件中的测试用例数据
test_cases = get_test_data("test_data")
print("test_cases: %s" % test_cases)
test_results = []

for test_case in test_cases:#逐一执行测试用例
    url = test_case[0]
    data = test_case[1]
    test_case_result = ""
    if '%' in data: # 如果有%，则说明需要处理关联
        data = after_data_handler(data)
    result_key = test_case[2]
    start_time = time.time()
    r = send_request(url,data)
    print("r.text: %s" % r.text)
    end_time = time.time()
    test_time = int((end_time - start_time) * 1000)
    total_test_case+=1
    if assert_result(r,result_key):
        success_test_case+=1
        test_case_result = "成功"
    else:
        failed_test_case+=1
        test_case_result = "失败"
    # 处理关联
    try:
        test_data_post_hander(r.text, test_case[3])
        print("关联获取变量成功")
    except:
        print("关联失败")
    test_results.append((r.url, data, r.text, test_time, test_case[2], test_case_result))
    print("test_results: %s" % test_results)

print("一共执行了%d个case" % total_test_case)
print("验证通过了%d个case" % success_test_case)
print("验证失败了%d个case" % failed_test_case)

html_name = '接口测试报告'
report_html(test_results, html_name)

#send_mail()

