//https://www.ntdm8.com/
var rule = {
    title: 'nt动漫',
    host: 'https://www.ntdm8.com',
    homeUrl: '/type/riben.html',
    url: '/type/fyclass-fypage.html',
    filterable: 0, //是否启用分类筛选,
    //filter_url: '--{{fl.by}}-{{fl.class}}--{{fl.letter}}---fypage---{{fl.year}}',
    searchUrl: '/vodsearch/-------------.html?wd=**',
    searchable: 2, //是否启用全局搜索,
    quickSearch: 1, //是否启用快速搜索,
    headers: { //网站的请求头,完整支持所有的,常带ua和cookies
        'User-Agent': 'MOBILE_UA',
    },
    timeout: 3000,
    class_parse: '.search-tag&&li;a&&Text;a&&href;.*/type/(.*?).html',
    cate_exclude: '',
    play_parse: true,
    detailUrl: '',
    lazy: "",
    limit: 6,
    推荐: '*',
    double: true, // 推荐内容是否双层定位
    一级: '.blockcontent1;img&&alt;img&&data-src;.newname&&Text;a&&href',//列表；名称；图片，剧集数；链接,
    二级访问前: '',
    二级: {
        "title": ".h3&&Text;.slide-info&&span&&Text",//名称；状态
        "img": ".lazy mask-1&&data-src",
        "content": "js:TABS=['懒得写']",//简介
        "tabs": "js:TABS=['小卢快线','天堂','🦌','少','点','了']",//线路名
        "lists": ".anthology-list-play:eq(#id)&&li"//列表
    },
    搜索: '*',
}