

var rule = {
    title: '圣城影视',
    host: 'https://www.sunnafh.com',
    homeUrl: '/',
    url: '/vodshow/fyclass--------fypage.html',
    detailUrl: '/voddetail/fyid.html',
    searchUrl: '/index.php?m=vod-search-wd-**keyword**-p-fypage.html',
    searchable: 2,
    quickSearch: 1,
    filterable: 0,
    headers: {'User-Agent': 'MOBILE_UA'},

    class_name: '电影&剧集&综艺&动漫',
    class_url: '1&2&3&4',

    play_parse: true,
    lazy: $js.toString(() => {
        let init_html = request(input, {headers:{'User-Agent':'Mozilla/5.0','Referer':rule.host}});
        let player_data = init_html.match(/player_aaaaa=({.+?})<\/script>/);
        if (!player_data) player_data = init_html.match(/var player_aaaaa=({.+?});/);
        if (!player_data) {
            input = {parse:0, url:input, jsLoadingInject: true};
            return;
        }
        let json = JSON.parse(player_data[1]);
        let real_url = json.url || '';
        let next_url = json.url_next || '';
        let play_url = real_url.startsWith('http') ? real_url : next_url;
        if (!play_url || play_url.includes('.m3u8') === false) {
            play_url = next_url || real_url;
        }
        input = {
            parse: 0,
            url: play_url,
            header: {
                'User-Agent': 'Mozilla/5.0',
                'Referer': 'https://www.sunnafh.com/'
            }
        };
    }),

    一级: '.module-item;.module-item-title a&&Text;.module-item-pic img&&data-src;.module-item-text&&Text;a&&href',
    二级: {
        title: 'h1&&Text;.tag-link:eq(0)&&Text',
        img: '.module-item-pic img&&data-src',
        desc: '.tag-link:eq(2)&&Text;;.tag-link:eq(1)&&Text;.module-info-item:eq(3) a&&Text;.module-info-item:eq(2) a&&Text',
        content: '.sqjj_a&&Text',
        tabs: '.module-tab-item span',
        lists: '.module-play-list:eq(#id) a',
        list_text: 'span&&Text',
        list_url: 'a&&href'
    },

    搜索: '.module-search-item;.video-name a&&Text;img&&data-src;.video-serial&&Text;a&&href',
}
