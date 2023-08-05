import json

from re_common.baselibrary.utils.core.requests_core import MsgCode


class MRequest(object):
    POST = "post"
    GET = "get"

    def __init__(self, logger=None):
        if logger is None:
            from re_common.baselibrary import MLogger
            logger = MLogger().streamlogger
        self.logger = logger
        self.html = None
        self.resp = None
        self.marks = []
        self.middler_list = [self.status_code_middlerwares, self.end_middlerwares, self.marks_middlerwares]
        self.status_code = None
        self.header = None
        self.refer = None
        self.proxy = None
        self.url = None
        self.params = None
        self.data = None
        self.cookie = None
        self.sn = None
        self.files = None
        self.auth = None
        self.timeout = None
        self.allow_redirects = True
        self.hooks = None
        self.stream = None
        self.verify = None
        self.cert = None
        self.json = None
        self.resp_dicts = {"code": self.status_code, "msg": ""}

    def set_html(self, html):
        """
        设置html
        :param html:
        :return:
        """
        self.html = html
        return self

    def set_status_code(self, status_code):
        """
        设置状态码
        :param status_code:
        :return:
        """
        self.status_code = status_code
        self.resp_dicts["code"] = self.status_code
        return self

    def set_middler_list(self, lists):
        """
        设置需要验证的步骤
        :param lists:
        :return:
        """
        self.middler_list = lists

    def set_marks(self, marks: list):
        """
        设置验证码
        :param marks:
        :return:
        """
        self.marks = marks
        return self

    def set_timeout(self, timeout):
        """
        设置超时
        :param timeout:
        :return:
        """
        self.timeout = timeout
        return self

    def set_header(self, header):
        """
        设置header
        :return:
        """
        self.header = header
        return self

    def set_refer(self, refer):
        """
        设置header中的refer，每次请求有可能变化
        :return:
        """
        self.refer = refer
        return self

    def set_proxy(self, proxy):
        """
        设置代理
        :return:
        """
        self.proxy = proxy
        return self

    def set_url(self, url):
        """
        设置请求的url
        :return:
        """
        self.url = url
        return self

    def set_params(self, params):
        """
        get 请求参数
        :return:
        """
        self.params = params
        return self

    def set_data(self, data):
        """
        设置请求参数
        :return:
        """
        self.data = data
        return self

    def set_cookie(self, cookie):
        """
        设置cookie
        :return:
        """
        self.cookie = cookie
        return self

    def set_sn(self, sn):
        """
        设置会话
        :return:
        """
        self.sn = sn
        return self

    def close_sn(self):
        """
        关闭会话
        :return:
        """
        if self.sn is not None:
            self.sn.close()

    def builder(self):
        """
        建造成需要的对象用于接下来请求使用
        :return:
        """
        if self.refer != "":
            self.header["refer"] = self.refer

    def get(self):
        """
        get 请求
        :return:
        """
        pass

    def post(self):
        """
        post 请求
        :return:
        """

    def on_request_start(self):
        """
        请求前的钩子函数
        :return:
        """

    def on_request_end(self):
        """
        请求结束的钩子函数
        :return:
        """

    def status_code_middlerwares(self, status_code=200):
        """
        验证返回码
        :return:
        """
        if self.status_code != status_code:
            self.resp_dicts["code"] = self.status_code
            self.resp_dicts["msg"] = "status_code err {}".format(self.status_code)
            return False, self.resp_dicts
        return True, self.resp_dicts

    def end_middlerwares(self, endstring="</html>"):
        """
        必须以什么结束
        :return:
        """
        if not self.html.endswith(endstring):
            self.resp_dicts["code"] = MsgCode.END_STRING_ERROR
            self.resp_dicts["msg"] = "not endswith {}".format(endstring)
            return False, self.resp_dicts
        return True, self.resp_dicts

    def have_end_middlerwares(self, havestring="</html>"):
        if self.html.find(havestring) == -1:
            self.resp_dicts["code"] = MsgCode.END_STRING_ERROR,
            self.resp_dicts["msg"] = "not have endswith {}".format(havestring)
            return False, self.resp_dicts
        return True, self.resp_dicts

    def marks_middlerwares(self):
        """
        建议至少两个，
        一个是id 防止因为cookie请求到其他的页面
        一个为验证该html关键词，用于改版预测
        :param marks: 一个列表
        :return:
        """
        mark_str = ""
        for mark in self.marks:
            if self.html.find(mark) == -1:
                mark_str = mark_str + mark + ";"

        if mark_str != "":
            self.resp_dicts["code"] = MsgCode.MARK_ERROR
            self.resp_dicts["msg"] = "mark Feature err: {}".format(mark_str)
            return False, self.resp_dicts
        else:
            return True, self.resp_dicts

    def is_json_middlerwares(self):
        """
        验证返回结果是否是json
        :return:
        """
        try:
            dic = json.loads(self.html)
        except Exception as e:
            self.resp_dicts["code"] = MsgCode.NOT_IS_JSON
            self.resp_dicts["msg"] = "not is json error, {}".format(repr(e))
            return False, self.resp_dicts
        return True, self.resp_dicts
