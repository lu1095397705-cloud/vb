var rule = {
    title: '木偶网盘',
    host: 'https://666.666291.xyz',
    url: '/index.php/vod/show/id/fyclass/page/fypage.html',
    searchUrl: '/index.php/vod/search/page/fypage/wd/**.html',
    searchable: 2,
    quickSearch: 0,
    filterable: 0,

    headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    },

    class_name: '木偶电影&木偶剧集&木偶动漫&木偶纪录',
    class_url: '1&2&3&4',

    一级: '#main .module-item;.module-item-pic img&&alt;.module-item-pic img&&data-src;.module-item-text&&Text;.module-item-pic a&&href',

    二级: {
        "title": ".page-title&&Text",
        "img": ".mobile-play .lazyload&&data-src",
        "desc": ".video-info-items:contains(导演)&&Text;.video-info-items:contains(主演)&&Text",
        "content": ".video-info-item:contains(剧情) .video-info-content&&Text",

        "tabs": `js:TABS=['网盘直链']`,

        // 🔴 修复部分：完全照搬 UZ 的逻辑
        // 1. 先拿到所有的 module-row-info
        // 2. 再取里面的 p 标签内容
        "lists": `js:
            var d = [];
            // 获取包含链接的容器 div
            var list = pdfa(html, '.module-row-info');
            
            list.forEach(function(it) {
                // 提取容器内 p 标签的文本
                var url = pdfh(it, 'p&&Text');
                // 去除可能存在的换行符和空格
                url = url.trim();
                
                // 只要有内容，就加进去
                if (url) {
                    d.push('点击播放$' + url);
                }
            });
            LISTS = [d];
        `
    },

    搜索: '.module-search-item;.video-serial&&title;.module-item-pic img&&data-src;.video-serial&&Text;.video-serial&&href',
}
