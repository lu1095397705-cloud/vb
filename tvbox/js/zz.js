// ==UserScript==
// name: 🔥MX动漫 FM专用版
// date: 2025-11-27 实测完美有数据
// ==/UserScript==

var rule = {
    title: '🔥MX动漫[FM专用]',
    host: 'https://www.mxdm.xyz',
    homeUrl: '/',
    url: '/type/fyclass.html',  // 分类页基础
    detailUrl: '/dongman/fyid.html',
    searchUrl: '/search/**------------.html',
    searchable: 2,
    quickSearch: 1,
    filterable: 0,
    headers: { 'User-Agent': 'MOBILE_UA' },

    class_name: '日本动漫&国产动漫&动漫电影&欧美动漫&专题',
    class_url: 'riman&guoman&dmdianying&oman&topic',

    一级: 'body; a[href*="/dongman/"]&&Text; ; p&&Text; a[href*="/dongman/"]&&href',  // 无图片，用空占位；FM严格适配
    二级: {
        "title": "h1&&Text",
        "img": "",  // 无图
        "desc": "p&&Text",
        "content": ".intro&&Text",
        "tabs": ".play-tab a",  // JS动态tab
        "lists": ".play-list:eq(#id) a",
        "list_text": "a&&Text",
        "list_url": "a&&href"
    },

    搜索: 'body; a[href*="/dongman/"]&&Text; ; p&&Text; a[href*="/dongman/"]&&href',

    play_parse: true,
    lazy: $js.toString(() => {
        let html = request(input, { headers: { 'User-Agent': 'Mozilla/5.0', 'Referer': rule.host } });
        // 匹配常见player JS
        let match = html.match(/player_aaaa=({.+?})/) || html.match(/var player = ({.+?})/);
        if (match) {
            let json = JSON.parse(match[1]);
            let url = json.url || json.src;
            if (url.startsWith('http')) {
                input = { parse: 0, url: url, header: { 'User-Agent': 'Mozilla/5.0' } };
                return;
            }
        }
        // 兜底直链
        input = { parse: 0, url: input, header: { 'User-Agent': 'Mozilla/5.0', 'Referer': rule.host } };
    })
}
