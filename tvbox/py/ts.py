# -*- coding: utf-8 -*-
# @Time    : 2024-05-23
# @Author  : AI Assistant
# @File    : template.py
# @Desc    : TVBox drpy爬虫通用模板, 带详细注释


rule = {

    'title': '新',
    'host': 'https://www.ntdm8.com',
    'hostJs': '',
    'headers': {  # 全局请求头, 用于模拟浏览器访问
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
       },


    'class_name': '小日本&&中国',
    'class_url': '/type/riben&&/type/zhongguo',
    'class_parse': '.search-tag&&li;a&&Text;a&&href;.*/(\w+).html',


    'homeContent': True,



    '一级': '.blockcontent1&&.blockdif2;img&&alt;img&&src;.newname&&Text;a&&href',

    '二级': {
        'title': 'h4&&Text;.detail_imform_value:eq(6)&&Text',  # 视频大标题
        'img': '.poster&&src',  # 视频封面图
        'desc': '',  # 描述, 通常包含年份/地区/类型等信息
        'content': '.detail_imform_desc_pre&&Text',  # 剧情简介
        # 'tabs': '.playlist-tabs&&a', # 播放源(线路)的Tab选择器, 比如"线路一"、"线路二"。
        # 'lists': '.playlist-group:eq(#id)&&a', # 播放列表选择器。:eq(#id)是固定写法, #id会被drpy替换成第几个tab。

        # 对于网盘类或者某些单播放源网站, 可以用JS来伪造播放列表
        'tabs': "js:TABS=['一线']", # 直接用JS创建一个名为"网盘资源"的播放源
        "lists": ".movurl:eq(#id)&&li"
        #'lists': "js:LISTS=[['立即播放$'+location.href]]",  # 直接用JS创建一个播放列表, 名字叫"立即播放", 链接就是当前详情页的URL。用于后续嗅探。
    },


    'searchUrl': '/search/**----------fypage---.html',  # 搜索链接模板。'**'是关键词占位符, 'fypage'是页码占位符。
    'searchable': 2,  # 0:不支持搜索, 1:支持快捷搜索, 2:支持聚合搜索
    'quickSearch': 1,  # 0:不支持, 1:支持
    '搜索': '',  # 搜索结果页的解析规则。如果留空, 会默认使用'一级'规则。格式与'一级'完全相同。

    # ------------------  播放解析配置  ------------------
    'play_parse': True,  # 是否开启内置解析。对于需要嗅探或解析的网站, 必须为True。
#'sniffer': True,  # 是否开启嗅探。对于网盘资源站, 必须为True, 它会自动嗅探页面中的网盘链接。
    'lazy': '',  # (高级功能)懒加载解析。通常是一个JS函数, 用于处理需要二次请求才能获取到真实播放地址的情况。
    # 示例1 (通用, 无特殊处理):
    # 'lazy': "js:input.endsWith('.m3u8')||input.endsWith('.mp4')?input:{parse:1,url:input}",
    # 示例2 (网盘站, 直接将详情页URL交给嗅探器):
    # 'lazy': "js:input={parse:0, url:input}",
}


# --- 以下为drpy引擎会自动调用的标准函数 ---
# 对于大多数网站, 你完全不需要修改以下任何代码
# 只有在遇到非常复杂的网站逻辑时, 才需要在这里编写自定义的Python代码

def init(ext):

    print("模板爬虫初始化...")

    pass


def homeContent(filter):

    print("正在获取首页内容...")
    pass


def homeVideoContent():

    pass


def categoryContent(tid, pg, filter, extend):

    print(f"正在获取分类 '{tid}' 的第 {pg} 页内容...")
    pass


def detailContent(array):

    print(f"正在获取详情页内容: {array[0]}")
    pass


def playerContent(flag, id, vipFlags):

    print(f"正在解析播放地址: flag={flag}, id={id}")

    return {
        'parse': 0,  # 0: 直接播放, 1: 网页嗅探, 2: JSON嗅探...
        'playUrl': '',  # 如果parse不为0, 这里可以为空
        'url': id,  # 要解析的URL, 通常就是传入的id
        'header': rule.get('headers')  # 传递请求头
    }


def searchContent(key, quick):

    print(f"正在搜索: {key} (快速搜索: {quick})")
    pass


def localSearch(key):

    pass

