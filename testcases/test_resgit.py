# -*- coding:utf8 -*-
# @Time   : 2019/5/5 15:32
# @author : wangchangguan
# @Email  ：1443112278@qq.com
# @File   : test_resgit.py
import unittest
from ddt import ddt,data

from api_2.commom import contant
from api_2.commom import do_excel
from api_2.commom import do_mysql
from api_2.commom import http_request
from api_2.commom import do_logging
logger = do_logging.do_logging(__name__)

@ddt
class TestResgiter(unittest.TestCase):
    excel = do_excel.DoExcel(contant.case_file,'register')
    cases = excel.get_cases()

    @classmethod
    def setUpClass(cls):
        cls.http_request = http_request.HttpRequest()
        cls.mysql = do_mysql.MySql()

    @data(*cases)
    def test_register(self,case):
        logger.info('开始执行用例：{0}----------'.format(case.title))
        if case.data.find('register_mobile') > -1 :   #判断参数化标识
            sql = 'select max(mobilephone) from future.member'
            max_phone = self.mysql.fetch_one_tuple(sql)[0]
            #最大手机号码加1
            max_phone = int(max_phone) + 1
            case.data = case.data.replace('register_mobile',str(max_phone))

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
        cls.mysql.close()