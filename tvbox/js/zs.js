var rule = {
    title: '木偶网盘',
    host: 'https://666.666291.xyz',
    url: '/index.php/vod/show/id/fyclass/page/fypage.html',
    searchUrl: '/index.php/vod/search/page/fypage/wd/**.html',
    searchable: 2,
    quickSearch: 0,
    filterable: 0,

    headers: {
        'User-Agent': 'Mozilla/5.0'
    },

    // 1. 分类写死
    class_name: '木偶电影&木偶剧集&木偶动漫&木偶纪录',
    class_url: '1&2&3&4',

    // 2. 列表解析
    一级: '#main .module-item;.module-item-pic img&&alt;.module-item-pic img&&data-src;.module-item-text&&Text;.module-item-pic a&&href',

    // 3. 详情解析（修改为最原始的 for 循环，防止报错）
    二级: {
        "title": ".page-title&&Text",
        "img": ".lazyload&&data-src",
        "desc": ".video-info-items:contains(导演)&&Text;.video-info-items:contains(主演)&&Text",
        "content": ".video-info-content&&Text",
        "tabs": "js:TABS=['网盘直链']",
        "lists": "js:var d=[];var list=pdfa(html,'.module-row-info p');for(var i=0;i<list.length;i++){var url=pdfh(list[i],'body&&Text').trim();if(url.indexOf('http')>-1){d.push('点击播放$'+url)}}LISTS=[d]"
    },

    搜索: '.module-search-item;.video-serial&&title;.module-item-pic img&&data-src;.video-serial&&Text;.video-serial&&href',
}
