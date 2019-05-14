# -*- coding:utf8 -*-
# @Time   : 2019/5/5 18:49
# @author : wangchangguan
# @Email  ：1443112278@qq.com
# @File   : test_invests.py
import unittest
from ddt import ddt,data

from api_2.commom import contant
from api_2.commom import do_excel
from api_2.commom import do_mysql
from api_2.commom import http_request
from api_2.commom import context
from api_2.commom.context import Context
from api_2.commom import do_logging
logger = do_logging.do_logging(__name__)

@ddt
class TestLogin(unittest.TestCase):
    excel = do_excel.DoExcel(contant.case_file,'invest')
    cases = excel.get_cases()

    @classmethod
    def setUpClass(cls):
        cls.http_request = http_request.HttpRequest()
        cls.mysql = do_mysql.MySql()

    @data(*cases)
    def test_register(self,case):
        logger.info('开始执行用例：{0}----------'.format(case.title))
        case.data = context.replace(case.data)
        resp = self.http_request.http_request(case.method,case.url,case.data)
        logger.info('请求返回的结果：{0}----------'.format(resp.text))
        actual_code = resp.json()['code']
        try:
            self.assertEqual(case.expected,int(actual_code))
            self.excel.write(case.case_id + 1,resp.text,'PASS')
            #判断加标成功之后，查询数据库，取到load_id
            if resp.json()['msg'] == '加标成功':
                sql = "select id from future.loan where memberid = 801 order by id desc limit 1"
                loan_id = self.mysql.fetch_one_dict(sql)['id']
                logger.info('标的ID：{0}'.format(loan_id))
                setattr(Context,"loan_id",str(loan_id))

        except AssertionError as e :
            self.excel.write(case.case_id + 1,resp.text,'FASLE')
            logger.error('和预期结果对比报错，错误为{0}'.format(e))
        logger.info('用例执行完成----------')

    @classmethod
    def tearDownClass(cls):
        cls.http_request.close()
        cls.mysql.close()