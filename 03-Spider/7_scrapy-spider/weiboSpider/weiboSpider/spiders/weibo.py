
import scrapy
import json

from scrapy import Request

from weiboSpider.items import WeiboUserItem, UserFollowerItem, UserFansItem


class WeoboSpider(scrapy.Spider):

    name = 'weibo'

    # 用户的 uid
    uids = [
        '1831216671',  # 黄磊
        '1749127163',  # 雷军
    ]

    # 用户
    user_url = r'https://m.weibo.cn/api/container/getIndex?uid={uid}&containerid=100505{uid}'
    # 关注
    flower_url = r'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&page={page}'
    # 粉丝
    fans_url = r'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&since_id={page}'

    def start_requests(self):
        """开始的 请求"""
        for uid in self.uids:
            yield Request(self.user_url.format(uid=uid), callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        if data['ok']:
            userInfo = data['data']['userInfo']
            user_item = WeiboUserItem()
            # 需要的字段
            need_params = (
                'id',  # 用户 id
                'screen_name', # 用户名
                'profile_image_url',  #
                'statuses_count',
                'verified',
                'gender',  # 性别
                'verified_type',
                'verified_type_ext',
                'verified_reason',  # 微博认证
                'close_blue_v',
                'description',   # 个人简介
                'follow_count',  # 关注的用户数
                'followers_count',  # 粉丝数
                'cover_image_phone',
                'avatar_hd', # 头像
            )

            for key in need_params:
                user_item[key] = userInfo.get(key)

            # 返回值 用户 item 进行下一步保存
            yield user_item

            # 发送请求获取关注的用户信息，使用 callback 进行解析响应
            yield Request(self.flower_url.format(uid=user_item.get('id'), page=1),
                         callback=self.parse_fllower,
                         meta={'uid': user_item['id'], 'page': 1})

            # 发送请求获取粉丝的信息，执行 callback 进行解析
            yield Request(self.fans_url.format(uid=user_item.get('id'), page=1),
                          callback=self.parse_fans,
                          meta={'uid': user_item['id'], 'page': 1})

    def parse_fllower(self, response):
        """
         目标用户所关注的 用户

        :param response: callback 中获取的响应
        :yield: 分布式获取内容
        """
        # 获取响应的文本， json 格式
        res = json.loads(response.text)
        if res['ok']:
            # 所属用户的 id 前面 meta 传入的参数
            uid = response.meta.get('uid')

            # 最后一个时关注的 人数
            card_group = res['data']['cards'][-1]['card_group']

            # 解析用户和关注人之间的关系, 得到关注的人的列表, 内部是字典
            # 当前页面的 20 个
            follower_list = []

            for card_info in card_group:
                user_info = card_info['user']
                id = user_info['id']
                name = user_info['screen_name']
                follower_list.append({'id': id, 'name': name})

                # 回调解析 uid  获取用户信息， 继续循环调用， 获取更多用户的信息，暂时不需要，可以无限循环
                # yield Request(self.user_url.format(uid=id), callback=self.parse)

            # 添加到 item 中
            user_follower = UserFollowerItem()
            user_follower['id'] = uid
            user_follower['follower'] = follower_list
            # 返回 user_relation， 进行下一步， pipeline 保存
            yield user_follower

            # 获取下一页
            page = int(response.meta.get('page')) + 1
            yield Request(self.flower_url.format(uid=uid,
                          page=page), callback=self.parse_fllower,
                          meta={'uid': uid, 'page': page})
        else:
            pass

    def parse_fans(self, response):
        """
        获取所属用户的 粉丝

        :param response: callback 中的 函数获取的响应
        :yield: 分布式获取内容
        """

        res = json.loads(response.text)
        if res.get('ok'):
            # 粉丝所属用户的 id
            uid = response.meta.get('uid')
            # 粉丝的列表，只保存粉丝的 id 和 screen_name
            fans_list = []

            card_group = res['data']['cards'][-1]['card_group']
            for card_info in card_group:
                fans = card_info['user']
                id = fans['id']
                name = fans['screen_name']
                # 将获取的信息添加到 粉丝列表中
                fans_list.append({'id': id, 'name': name})

                # 继续使用回调， 进行获取粉丝的详情，暂时不用，可以无限循环
                # yield Request(self.user_url.format(uid=id), callback=self.parse)

            user_fans = UserFansItem()
            user_fans['id'] = uid
            user_fans['fans'] = fans_list
            # 返回数据, 保存数据库
            yield user_fans

            # 下一页  粉丝可能会很多 几千万 ， 设置简单的条件， 暂时获取 10 页  200 条
            page = int(response.meta.get('page')) + 1
            # if page <= 10:
            yield Request(self.fans_url.format(uid=uid,page=page),
                          callback=self.parse_fans,
                          meta={'uid': uid, 'page': page})
        else:
            pass
