var rule = {
    title: '木偶网盘',
    host: 'https://666.666291.xyz',
    // 列表页 URL：对应 UZ 的 /index.php/vod/show/id/${args.url}/page/${args.page}.html
    url: '/index.php/vod/show/id/fyclass/page/fypage.html',
    // 搜索 URL：对应 UZ 的 /index.php/vod/search/page/${args.page}/wd/${args.searchWord}.html
    searchUrl: '/index.php/vod/search/page/fypage/wd/**.html',
    searchable: 2,
    quickSearch: 0,
    filterable: 0,

    headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    },

    // 1. 分类：对应 UZ 脚本里的 getClassList
    class_name: '木偶电影&木偶剧集&木偶动漫&木偶纪录',
    class_url: '1&2&3&4',

    // 2. 列表页解析：对应 UZ 脚本里的 getVideoList
    // 容器: #main .module-item
    // 标题: img&&alt
    // 图片: img&&data-src
    // 描述: .module-item-text&&Text
    // 链接: .module-item-pic a&&href
    一级: '#main .module-item;.module-item-pic img&&alt;.module-item-pic img&&data-src;.module-item-text&&Text;.module-item-pic a&&href',

    // 3. 详情页解析：对应 UZ 脚本里的 getVideoDetail
    二级: {
        "title": ".page-title&&Text",
        "img": ".mobile-play .lazyload&&data-src",
        // 对应脚本里提取 剧情、导演、主演 的逻辑，这里简化抓取
        "desc": ".video-info-items:contains(导演)&&Text;.video-info-items:contains(主演)&&Text",
        "content": ".video-info-item:contains(剧情) .video-info-content&&Text",

        // 自定义 Tab 名字
        "tabs": `js:TABS=['网盘直链']`,

        // 核心：提取网盘链接
        // UZ源码逻辑：$('.module-row-info').find('p')[0].children[0].data
        // 这里我们遍历 .module-row-info p，取出里面的 http 链接
        "lists": `js:
            log(html);
            var d = [];
            // 获取所有包含链接的 p 标签
            var list = pdfa(html, '.module-row-info p');
            for (var i = 0; i < list.length; i++) {
                // 提取 p 标签内的文本 (即 URL)
                var url = pdfh(list[i], 'p&&Text');
                // 简单清洗，确保是链接
                if (url && url.indexOf('http') > -1) {
                    d.push('点击播放/转存$' + url);
                }
            }
            LISTS = [d];
        `
    },

    // 4. 搜索解析：对应 UZ 脚本里的 searchVideo
    // 容器: .module-search-item
    // 标题: .video-serial&&title
    // 图片: .module-item-pic img&&data-src
    // 备注: .video-serial&&Text
    // 链接: .video-serial&&href
    搜索: '.module-search-item;.video-serial&&title;.module-item-pic img&&data-src;.video-serial&&Text;.video-serial&&href',
}
