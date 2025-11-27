// ==UserScript==
// name: 🌙圣城影视FM专用版
// date: 2025-12-20 FM壳子实测完美有图
// ==/UserScript==

var rule = {
    title: '🌙圣城影视[FM专用]',
    host: 'https://www.sunnafh.com',
    homeUrl: '/',
    url: '/vodshow/fyclass--------fypage---.html',
    detailUrl:'/voddetail/fyid.html',
    searchUrl: '/vodsearch/-------------.html?wd=**&submit=',
    searchable: 2,
    quickSearch: 1,
    filterable: 0,
    headers: {'User-Agent': 'MOBILE_UA'},

    class_name: '电影&连续剧&综艺&动漫&纪录片',
    class_url: '1&2&3&4&20',

    一级: '.module-item;.module-item-title&&Text;.lazyload&&data-original;.module-item-note&&Text;.module-item-title a&&href',  // FM最严格的写法
    二级: {
        "title": ".video-title&&Text;.video-info-aux a&&Text",
        "img": ".lazyload&&data-original",
        "desc": ".video-info-items:eq(3)&&Text;;.video-info-items:eq(1)&&Text;.video-info-items:eq(2)&&Text",
        "content": ".sqjj_a&&Text",
        "tabs": ".module-tab-item span",
        "lists": ".module-play-list:eq(#id) a",
        "list_text": "span&&Text",
        "list_url": "a&&href"
    },

    搜索: '.module-card-item;.module-card-item-title a&&Text;.lazyload&&data-original;.module-info-tag&&Text;a&&href',

    play_parse: true,
    lazy: $js.toString(() => {
        let html = request(input, {headers:{'User-Agent':'Mozilla/5.0','Referer':rule.host}});
        let config = html.match(/player_aaaa=({.+?})/);
        if(!config) config = html.match(/player_aaaaa=({.+?})/);
        if(config){
            let json = JSON.parse(config[1]);
            let url = json.url;
            if(url.startsWith('http')){
                input = {parse:0, url:url, header:{'User-Agent':'Mozilla/5.0'}};
                return;
            }
        }
        // 兜底直链
        input = {parse:0, url:input, header:{'User-Agent':'Mozilla/5.0','Referer':rule.host}};
    })
}
