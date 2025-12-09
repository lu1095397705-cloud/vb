var rule = {
    title: '米却影视[网盘]',
    host: 'http://www.miqk.cc',
    url: '/type/fyclass-fypage.html',
    searchUrl: '/search/-------------.html?wd=**',
    searchable: 2,
    quickSearch: 0,
    filterable: 0,

    headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'http://www.miqk.cc/'
    },

    // 自动获取分类
    class_parse: '.myui-header__menu li.dropdown;a&&Text;a&&href;/type/(\\d+).html',

    // 列表页解析（和之前一样，这部分没问题）
    推荐: '.myui-vodlist__box;a&&title;a&&data-original;.pic-text&&Text;a&&href',
    一级: '.myui-vodlist__box;a&&title;a&&data-original;.pic-text&&Text;a&&href',

    二级: {
        "title": "h1.title&&Text;.data:eq(0)&&Text",
        "img": ".myui-content__thumb .lazyload&&data-original",
        "desc": ".data:eq(-2)&&Text;.data:eq(-1)&&Text",
        "content": ".data:eq(3)&&Text",

        // 1. 抓取“网盘下载”或“在线播放”的 Tab
        "tabs": ".nav-tabs:eq(0) li",

        // 2. 重点：直接抓取 a 标签的 href（网盘链接），而不是让它去播放
        // 这里的 parsing 逻辑是：找到列表里的链接，作为视频地址返回
        "lists": ".myui-content__list:eq(#id) li a&&href"
    },

    // 搜索解析
    搜索: '.myui-vodlist__media;h4&&title;a&&data-original;.pic-text&&Text;a&&href',
}
