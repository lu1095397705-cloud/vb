// ==UserScript==
// @name         MX动漫 mxdm.xyz
// @version      2025.11.28
// @author       C1O
// @description  MX动漫（https://www.mxdm.xyz）- 在线动漫樱花备用，高清无广告
// @homeUrl      https://www.mxdm.xyz
// @rule         https?://www.mxdm.xyz
// @require      https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.min.js
// ==/UserScript==

var rule = {
    title: 'MX动漫',
    host: 'https://www.mxdm.xyz',
    homeUrl: '/', // 首页默认显示更新/热播
    url: '/type/fyclass-fypage.html', // 分类页（需调整为实际 type 路径）
    searchUrl: '/search/**------------fypage.html', // 搜索 URL 模式
    searchable: 2,
    quickSearch: 1,
    filterable: 1,
    headers: { 'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15' }, // 模拟移动 UA，避免 PC 版差异
    timeout: 5000,
    class_name: '日本动漫&国产动漫&动漫电影&欧美动漫&专题&萌图',
    class_url: '/type/riman.html&/type/guoman.html&/type/dmdianying.html&/type/oman.html&/topic.html&/arttype/mengtu.html',

    // 首页推荐（今日更新 + 热播）
    homeVod: {
        "今日更新": ".update-list a&&title;.update-list img&&src;a&&href",
        "正在热播": ".hot-list a&&title;.hot-list img&&src;a&&href"
    },

    // 一级（分类页）- 匹配站点列表结构
    一级: 'body;a&&Text;img&&src;a&&href;.item-desc&&Text', // 标题;海报;链接;简介（基于 <a> 和 <p> 结构）

    // 二级（详情页）- 提取标题/简介，集数需手动（站点更新至X集）
    二级: {
        "title": "h1&&Text", // 主标题
        "img": ".poster img&&src", // 海报（若无，用默认）
        "desc": ".intro&&Text", // 剧情简介（从 <p> 提取）
        "content": ".detail-info&&Text", // 演员/更新集数等
        "tabs": ".episode-tabs li", // 集数 tab（若有 JS 加载）
        "lists": ".episode-list a",
        "list_name": "a&&Text",
        "list_url": "a&&href"
    },

    // 搜索 - 匹配搜索结果列表
    搜索: 'body;a&&Text;img&&src;.search-desc&&Text;a&&href',

    // 播放解析（站点可能用 JS 加密，启用嗅探；或自定义提取 m3u8）
    sniffer: true, // 启用 TVBox 嗅探
    sniff_url: 'http://127.0.0.1:9978', // 默认嗅探端口（需 TVBox 配置）
    lazy: `js: // 备用懒加载：尝试提取页面内 m3u8 或 mp4
        let html = request(input);
        let m3u8 = html.match(/src=[\\"\\'](https?:\\/\\/[^\\"\\']*\\.m3u8[^\\"\\']*)[\\"\\']/);
        if (m3u8) {
            input = { parse: 0, url: m3u8[1], js: '' };
        } else {
            // 若无，fallback 到嗅探
            setError('使用嗅探提取播放源');
        }`,

    // 过滤（站点支持年份/地区少量筛选）
    推荐: '*',
    double: true,
    图片来源: '@Referer=https://www.mxdm.xyz@LazyRule=',

    // 分类筛选（基于年份/地区/类型）
    filter: {
        "riman": [{ "key": "year", "name": "年份", "value": [{ "n": "全部", "v": "" }, { "n": "2025", "v": "2025" }, { "n": "2024", "v": "2024" }, { "n": "2023", "v": "2023" }] }, { "key": "area", "name": "地区", "value": [{ "n": "日本", "v": "日本" }, { "n": "其他", "v": "其他" }] }],
        "guoman": [{ "key": "year", "name": "年份", "value": [{ "n": "全部", "v": "" }, { "n": "2025", "v": "2025" }, { "n": "2024", "v": "2024" }] }, { "key": "area", "name": "地区", "value": [{ "n": "大陆", "v": "大陆" }] }],
        "dmdianying": [{ "key": "year", "name": "年份", "value": [{ "n": "全部", "v": "" }, { "n": "2025", "v": "2025" }, { "n": "2024", "v": "2024" }] }],
        "oman": [{ "key": "year", "name": "年份", "value": [{ "n": "全部", "v": "" }, { "n": "2025", "v": "2025" }] }],
        "topic": [{ "key": "by", "name": "排序", "value": [{ "n": "时间", "v": "time" }, { "n": "人气", "v": "hits" }] }],
        "mengtu": [{ "key": "by", "name": "排序", "value": [{ "n": "时间", "v": "time" }] }
    }
};