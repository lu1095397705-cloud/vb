var rule = {
    title: 'SunnaFH',
    host: 'https://www.sunnafh.com',
    // 网站通常使用 lazyload，图片在 data-original 中
    // 列表页地址格式: /vodtype/分类ID-页码.html
    url: '/vodtype/fyclass-fypage.html',
    // 搜索地址: 使用 wd 参数
    searchUrl: '/vodsearch/-------------.html?wd=**',
    searchable: 2, // 1=可搜, 2=启用搜索
    quickSearch: 0, // 1=允许快速搜索
    filterable: 0, // 1=启用筛选
    headers: {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G9600 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36',
        'Referer': 'https://www.sunnafh.com/'
    },
    // 首页分类定义 (也可以写 automated 自动获取，这里手动定义更稳定)
    class_name: '电影&电视剧&综艺&动漫&纪录片',
    class_url: '1&2&3&4&5',

    // 推荐内容 (首页) 解析规则
    // 格式: 列表选择器;标题;图片;描述;链接
    推荐: '.stui-vodlist__box; a&&title; a&&data-original; .pic-text&&Text; a&&href',

    // 一级列表页解析规则
    // 格式: 列表选择器;标题;图片;描述;链接
    // 注意: 该站使用的是 .stui-vodlist__box 或者 .stui-vodlist__item
    limit: 6,
    double: true, // 是否双层解析，通常设为 true 兼容性更好
    一级: '.stui-vodlist__box; a&&title; a&&data-original; .pic-text&&Text; a&&href',

    // 二级详情页解析规则
    二级: {
        // 标题
        title: 'h1.title&&Text;.data:eq(0)&&Text',
        // 图片
        img: '.stui-content__thumb a&&data-original',
        // 描述
        desc: '.data:eq(-1)&&Text;.data:eq(-2)&&Text;.data:eq(-3)&&Text',
        // 内容简介
        content: '.stui-content__desc&&Text',
        // 线路数组 (播放源)
        tabs: '.nav-tabs li a',
        // 播放列表数组 (集数)
        lists: '.stui-content__playlist:eq(#id) li',
    },

    // 搜索结果解析规则
    // 搜索页面的结构通常和列表页略有不同，这里适配通用 stui 搜索列表
    搜索: '.stui-vodlist__media li; a&&title; a&&data-original; .pic-text&&Text; a&&href',
}
