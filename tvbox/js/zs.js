var rule = {
    title: '木偶网盘',
    host: 'https://666.666291.xyz',
    url: '/index.php/vod/show/id/fyclass/page/fypage.html',
    searchUrl: '/index.php/vod/search/page/fypage/wd/**.html',
    searchable: 2,
    quickSearch: 0,
    filterable: 0,
    headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    },

    // 1. 写死分类（最稳妥，防止分类解析失败）
    class_name: '电影&剧集&动漫&综艺&纪录片',
    class_url: '1&2&3&20&4',

    // 2. 列表页解析
    play_parse: true,
    lazy: '',
    limit: 6,
    推荐: '.module-list;.module-items .module-item;a&&title;img&&data-src;.module-item-text&&Text;a&&href',
    double: true, // 推荐是否双层结构
    一级: '.module-items .module-item;a&&title;img&&data-src;.module-item-text&&Text;a&&href',

    // 3. 详情页解析（核心修复部分）
    二级: {
        "title": "h1&&Text;.video-info-aux&&Text",
        "img": ".module-item-pic img&&data-src",
        "desc": ".video-info-items:eq(0)&&Text;.video-info-items:eq(1)&&Text;.video-info-items:eq(2)&&Text",
        "content": ".video-info-content&&Text",
        // 手动定义 Tab，防止自动识别出错
        "tabs": "js:TABS=['夸克网盘', '阿里云盘']",
        // 提取链接的逻辑
        "lists": `js:
            log(input);
            var d = [];
            // 获取包含链接的文本区域
            var html = pdfh(html, '.module-row-info&&Html');
            // 使用正则提取所有http开头的链接
            var links = html.match(/https?:\\/\\/[a-zA-Z0-9\\.\\/\\-_]+/g);
            
            if (links) {
                for (var i = 0; i < links.length; i++) {
                    var u = links[i];
                    // 只保留夸克和阿里的链接
                    if (u.indexOf('pan.quark') > -1 || u.indexOf('aliyundrive') > -1) {
                         d.push('点击跳转播放$' + u);
                    }
                }
            }
            // 将同一组链接复制给两个Tab，确保不为空
            LISTS = [d, d];
        `
    },

    // 4. 搜索解析
    搜索: '.module-search-item;h3&&Text;.lazyload&&data-src;.video-serial&&Text;a&&href',
}
