// name: 🌙圣城影视（2025.12最新版）
// date: 2025-12-08 实测完美运行

var rule = {
    title: '🌙圣城影视',
    host: 'https://www.sunnafh.com',
    homeUrl: '/',
    url: '/vodshow/fyclass--------fypage---.html',
    detailUrl: '/voddetail/fyid.html',
    searchUrl: '/vodsearch/**----------fypage---.html',
    searchable: 2,
    quickSearch: 1,
    headers: {'User-Agent': 'MOBILE_UA'},

    class_name: '电影&剧集&综艺&动漫&纪录片',
    class_url: '1&2&3&4&20',

    play_parse: true,
    lazy: $js.toString(() => {
        // 直接请求播放页
        let html = request(input, {
            headers: {
                'User-Agent': 'Mozilla/5.0',
                'Referer': 'https://www.sunnafh.com/'
            }
        });

        // 新版加密参数在 script 里
        let config = html.match(/r player_aaaa=({[^}]+})/);
        if (config && config[1]) {
            let json = JSON.parse(config[1]);
            let url = json.url || '';
            if (url) {
                if (url.startsWith('http')) {
                    input = { parse:0, url: url, header: rule.headers};
                } else if (json.encrypt && json.url) {
                    // 极少数情况走解密
                    let decrypted = crypto.decrypt(url, json.encrypt == 1 ? 'aes' : 'des', '12345678');
                    input = { parse:0, url: decrypted};
                }
            }
        }

        // 兜底：直接播放原地址（新版很多已经是直链）
        if (!input || !input.url) {
            input = { parse:0, url: input, header: {'User-Agent': 'Mozilla/5.0', 'Referer': rule.host}};
        }
    }),

    一级: '.module-items .module-item;img&&alt;img&&data-src;.module-item-text&&Text;a&&href',
    二级: {
        title: 'h1&&Text;.video-info-aux a:eq(0)&&Text',
        img: '.module-item-pic img&&data-src',
        desc: '.video-info-items:eq(3)&&Text;;.video-info-items:eq(1)&&Text;.video-info-items:eq(2)&&Text;.video-info-items:eq(0)&&Text',
        content: '.sqjj_a&&Text',
        tabs: '.module-tab-items .module-tab-item',
        lists: '.module-play-list:eq(#id) a',
        list_text: 'span&&Text',
        list_url: 'a&&href'
    },

    搜索: '.module-search-item;.video-name a&&Text;img&&data-src;.video-serial&&Text;a&&href',
}
