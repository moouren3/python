# -*- coding:utf8 -*-
# @Time   : 2019/5/5 16:05
# @author : wangchangguan
# @Email  ：1443112278@qq.com
# @File   : test_login.py
import unittest
from ddt import ddt,data

from api_2.commom import contant
from api_2.commom import do_excel
from api_2.commom import do_mysql
from api_2.commom import http_request
from api_2.commom import do_logging

logger = do_logging.do_logging(__name__)

@ddt
class TestLogin(unittest.TestCase):
    excel = do_excel.DoExcel(contant.case_file,'login')
    cases = excel.get_cases()

    @classmethod
    def setUpClass(cls):
        cls.http_request = http_request.HttpRequest()

    @data(*cases)
    def test_register(self,case):
        logger.info('开始执行用例：{0}----------'.format(case.title))
        resp = self.http_request.http_request(case.method,case.url,case.data)

        try:
            self.assertEqual(case.expected,resp.text)
            self.excel.write(case.case_id + 1,resp.text,'PASS')
        except AssertionError as e :
            self.excel.write(case.case_id + 1,resp.text,'FASLE')
            raise e
        logger.info('用例执行完成----------')

    @classmethod
    def tearDownClass(cls):
        cls.http_request.close()

