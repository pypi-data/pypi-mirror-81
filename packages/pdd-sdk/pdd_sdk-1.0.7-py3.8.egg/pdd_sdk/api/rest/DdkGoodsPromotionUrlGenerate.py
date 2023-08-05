# -*- coding: utf-8 -*-
# @Time    : 2018-12-09 14:27
# @Author  : play4fun
# @File    : DdkGoodsPromotionUrlGenerate.py
# @Software: PyCharm

"""
DdkGoodsPromotionUrlGenerate.py:
生成普通商品推广链接
"""

from pdd_sdk.api.base import RestApi


class DdkGoodsPromotionUrlGenerate(RestApi):
    def __init__(self, domain='gw-api.pinduoduo.com', port=80):
        RestApi.__init__(self, domain, port)
        # 自定义参数，为链接打上自定义标签；自定义参数最长限制64个字节；格式为： {"uid":"11111","sid":"22222"} ，
        # 其中 uid 用户唯一标识，可自行加密后传入，每个用户仅且对应一个标识，必填； sid 上下文信息标识，例如sessionId等，非必填。该json字符串中也可以加入其他自定义的key
        self.custom_parameters = None  

        
        self.generate_mall_collect_coupon = None # 布尔类型，是否生成店铺收藏券推广链接
        self.generate_qq_app = None # 布尔类型，是否生成qq小程序
        self.generate_schema_url = None # 布尔类型，是否返回 schema URL
        self.generate_short_url = None  # 布尔类型，是否生成短链接
        self.generate_weapp_webview = None  # 布尔类型，是否生成唤起微信客户端链接，true-是，false-否，默认false
        self.generate_weiboapp_webview = None # 布尔类型，是否生成微博推广链接
        self.generate_we_app = None # 布尔类型，是否生成小程序推广

        self.goods_id_list = None  # 商品ID，仅支持单个查询。例如：[123456]
        self.multi_group = None
        self.p_id = None  # 推广位id

        # true--生成多人团推广链接 false--生成单人团推广链接（默认false）1、单人团推广链接：用户访问单人团推广链接，可直接购买商品无需拼团。
        # 2、多人团推广链接：用户访问双人团推广链接开团，若用户分享给他人参团，则开团者和参团者的佣金均结算给推手
        self.multi_group = None  

        self.search_id = None  # 搜索id，建议填写，提高收益。来自pdd.ddk.goods.recommend.get、pdd.ddk.goods.search、pdd.ddk.top.goods.list.query等接口
        self.zs_duo_id = None  # 招商多多客ID

    def getapiname(self):
        return 'pdd.ddk.goods.promotion.url.generate'
