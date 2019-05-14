# -*- coding:utf8 -*-
# @Time   : 2019/5/5 16:09
# @author : wangchangguan
# @Email  ：1443112278@qq.com
# @File   : test_recharge.py
import unittest
from ddt import ddt, data

from api_2.commom import contant
from api_2.commom import do_excel
from api_2.commom import do_mysql
from api_2.commom import http_request
from api_2.commom import do_logging

logger = do_logging.do_logging(__name__)

@ddt
class TestLogin(unittest.TestCase):
    excel = do_excel.DoExcel(contant.case_file, 'recharge')
    cases = excel.get_cases()

    @classmethod
    def setUpClass(cls):
        cls.http_request = http_request.HttpRequest()
        cls.mysql = do_mysql.MySql()

    @data(*cases)
    def test_register(self, case):
        logger.info('开始执行用例：{0}----------'.format(case.title))
        if case.sql is not None:
            sql = eval(case.sql)['sql1']
            member = self.mysql.fetch_one_dict(sql)
            before_amount = member['LeaveAmount']

        resp = self.http_request.http_request(case.method, case.url, case.data)
        actual_code = resp.json()['code']

        try:
            self.assertEqual(case.expected, int(actual_code))
            self.excel.write(case.case_id + 1, resp.text, 'PASS')
            if case.sql is not None:
                sql = eval(case.sql)['sql1']
                member = self.mysql.fetch_one_dict(sql)
                after_amount = member['LeaveAmount']
                recharge_amount = int(eval(case.data)['amount'])
                self.assertEqual(before_amount + recharge_amount,after_amount)
        except AssertionError as  e:
            self.excel.write(case.case_id + 1, resp.text, 'FASLE')
            raise e
        logger.info('用例执行完成----------')

    @classmethod
    def tearDownClass(cls):
        cls.http_request.close()
        cls.mysql.close()

