//https://www.mxdm.xyz/
var rule ={
    title: 'mx动漫',
    host: 'https://www.mxdm.xyz',
    homeUrl: '/type/riman.html',
    url: '/show/fyclass--------fypage---.html',
    filterable: 0, //是否启用分类筛选,
    //filter_url: '--{{fl.by}}-{{fl.class}}--{{fl.letter}}---fypage---{{fl.year}}', 
    searchUrl: '/search/-------------.html?wd=**',
    searchable: 2, //是否启用全局搜索,
    quickSearch: 1, //是否启用快速搜索,
    headers: { //网站的请求头,完整支持所有的,常带ua和cookies
        'User-Agent': 'MOBILE_UA',
    },
    timeout: 5000,
    class_parse: '.nav-menu-items&&li:gt(0):lt(5);a&&title;a&&href;.*/(\\w+).html',
    play_parse: true,
    detailUrl: '',
    lazy: "",
    limit: 6,
    推荐: '*',
    double: true, // 推荐内容是否双层定位
    一级: '.module-items&&.module-item;.module-item-titlebox&&a&&title;img&&data-src;.module-item-text&&Text;a&&href',//列表；名称；图片，剧集数；链接,
    二级访问前: '',
    二级: {
        "title": "h1&&Text;.video-info-item:eq(2)&&Text",//名称；类型
        "img": "",
        "desc": "",
        "content": "",//简介
        "tabs": "js:TABS=['小卢快线','小卢二线','🦌','少','点','了']",//线路
        "lists": "#glist-1&&.scroll-content:eq(#id)"//列表
    },
    搜索: '*',

}