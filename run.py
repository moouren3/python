# -*- coding:utf8 -*-
# @Time  :2019/5/7 18:19
# @author :wangchangguan
# @Email  :1443112278@qq.com
# @File   :run.py

#用例
import unittest

from api_2.commom import HTMLTestRunnerNew
from api_2.commom import contant

discover = unittest.defaultTestLoader.discover(contant.case_dir,"test*.py")

with open(contant.report_dir + '/report.html','wb+') as file:
    runner = HTMLTestRunnerNew.HTMLTestRunner(stream=file,
                                              title="python15 api test report",
                                              description='部分接口自动化的报告',
                                              tester='wang')
    runner.run(discover)
