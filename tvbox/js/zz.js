var rule = {
    title:'MiQK影视',
    host:'https://www.miqk.cc',
    // 首页推荐（懒加载，抓取前几页）
    homeUrl: 'https://www.miqk.cc',  // 首页
    // 分类（示例：1=电影, 2=电视剧；实际从首页抓）
    classUrl: 'https://www.miqk.cc/vodtype/{cateId}-{page}.html',  // {cateId}={1}, {page}
    classParse: '.myui-header__title a || .stui-header__title a',  // 分类标题选择器

    // 推荐/首页视频列表
    recommend: {
        url: 'https://www.miqk.cc/index_{page}.html',  // 分页
        parse: [{
            title: 'ul.myui-vodlist li || ul.stui-vodlist li',  // 列表容器
            cols: [{
                // 推荐列表项
                url: './a.myui-vodlist__thumb || ./a.stui-vodlist__thumb',  // 详情链接
                title: 'a.myui-vodlist__thumb || a.stui-vodlist__thumb',  // 标题
                pic_url: 'img.lazy || img',  // 海报
                desc: './span.pic-text || ./span.text-muted'  // 描述（年份/地区）
            }]
        }]
    },

    // 分类视频列表
    category: {
        url: 'https://www.miqk.cc/vodtype/{cateId}-{page}.html',  // 分类分页
        parse: [{
            title: '.myui-vodlist li || .stui-vodlist li',
            cols: [{
                url: './a.myui-vodlist__thumb || ./a.stui-vodlist__thumb',
                title: 'a.myui-vodlist__thumb || a.stui-vodlist__thumb',
                pic_url: 'img.lazy || img',
                desc: './span.pic-text || ./span.text-muted'
            }]
        }]
    },

    // 搜索
    searchUrl: 'https://www.miqk.cc/search/-------------.html?wd=**',  // **=搜索词
    search: {
        url: 'https://www.miqk.cc/search/-------------.html?wd=**',
        parse: [{
            title: '.search-list ul li || .search-content ul li',
            cols: [{
                url: './a.myui-vodlist__thumb || ./a',
                title: 'a.myui-vodlist__thumb || a',
                pic_url: 'img.lazy || img',
                desc: './span.pic-text || ./span'
            }]
        }]
    },

    // 详情页
    detailUrl: 'https://www.miqk.cc/voddetail/{tid}.html',  // {tid}=id
    detail: {
        tabs: '.myui-panel__head h3 || .stui-panel__head h3',  // 标签页（剧集/演员等）
        lists: '.myui-panel__bd .scroll-content || .stui-panel__bd ul',  // 内容列表
        tabTitle: '.myui-panel__head-top h3 || .stui-panel__head-top h3',  // 标签标题
        content: '.myui-content__item || .stui-content__item',  // 剧集项
        url: './a || a',  // 播放链接
        title: './a || a',  // 剧集标题
        more: '.myui-link__text || .stui-link__text'  // 更多按钮
    },

    // 播放页（嗅探或直链）
    playUrl: '',  // 空=自动嗅探
    player: {
        // 如果有直链规则，添加这里；否则用 TVBox 默认嗅探
        parse: function(url) {
            // 示例：如果播放页有 iframe，提取 src
            var html = fetch(url, {headers: {'User-Agent': 'Mozilla/5.0'}});
            var iframe = html.match(/<iframe src="([^"]+)"/);
            if (iframe) return iframe[1];
            // 或 m3u8: html.match(/\.m3u8/)[0]
            return url;  // 默认返回原 URL 嗅探
        }
    },

    // 过滤（可选，既然不滤广告，保持原样）
    filter: null,

    // 全局 UA（防反爬）
    headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
};