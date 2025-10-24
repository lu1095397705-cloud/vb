//https://www.zjkrmv.com/
var rule = {
    title: '看片狂人',
    host: 'https://www.zjkrmv.com',
    homeUrl: '/vodshow/fyclass-----------.html',
    url: '/vodshow/fyclass--------fypage---.html',
    filterable: 0, //是否启用分类筛选,
    //filter_url: '--{{fl.by}}-{{fl.class}}--{{fl.letter}}---fypage---{{fl.year}}',
    searchUrl: '/vodsearch/-------------.html?wd=**',
    searchable: 2, //是否启用全局搜索,
    quickSearch: 0, //是否启用快速搜索,
    headers: { //网站的请求头,完整支持所有的,常带ua和cookies
        'User-Agent': 'MOBILE_UA',
    },
    timeout: 3000,
    class_parse: '.swiper-wrapper li;a&&Text;a&&href;.*/(.*?).html',
    cate_exclude: '午夜',
    play_parse: true,
    detailUrl: '',
    lazy: "",
    limit: 6,
    推荐: '*',
    double: true, // 推荐内容是否双层定位
    一级: '.public-list-div;.public-list-exp&&title;img&&data-src;.public-list-prb&&Text;a&&href',//列表；名称；图片，剧集数；链接,
    二级访问前: '',
    二级: {
        "title": ".h3&&Text;.slide-info&&span&&Text",//名称；状态
        "img": ".lazy mask-1&&data-src",
        "content": "",//简介
        "tabs": ".aria-label",//线路名
        "lists": ".anthology-list-play:eq(#id)&&li"//列表
    },
    搜索: '*',
}