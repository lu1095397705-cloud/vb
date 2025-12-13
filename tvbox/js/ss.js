//https://www.ntdm8.com/
var rule = {
    title: '玩偶',
    host: 'https://wogg.xxooo.cf/',
    homeUrl: '/vodtype/fyclass.html',
    url: '/vodshow/fyclass--------fypage---.html',
    filterable: 0, //是否启用分类筛选,
    //filter_url: '--{{fl.by}}-{{fl.class}}--{{fl.letter}}---fypage---{{fl.year}}',
    searchUrl: '/vodsearch/-------------.html?wd=**',
    searchable: 2, //是否启用全局搜索,
    quickSearch: 1, //是否启用快速搜索,
    headers: { //网站的请求头,完整支持所有的,常带ua和cookies
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    },
    timeout: 5000,
    class_parse: '.nav-menu-items li;a&&title;a&&href;.*/(.*?)/.html',
    cate_exclude: '推荐',
    play_parse: true,
    detailUrl: '',
    lazy: "",
    limit: 6,
    推荐: '*',
    double: true, // 推荐内容是否双层定位
    一级: '.module-item&&.module-item-pic;img&&alt;img&&data-src;.module-item-text&&Text;a&&href',//列表；名称；图片，剧集数；链接,
    二级访问前: '',
    二级: {
        "title": "h4&&Text;.detail_imform_value:eq(6)&&Text",//名称；状态
        "img": ".poster&&src",
        "desc": "",
        "content": ".detail_imform_desc_pre&&Text",//简介
        "tabs": "js:TABS=['小卢快线','小卢二线','🦌','少','点','了']",//线路名
        "lists": ".movurl:eq(#id)&&li"//列表
    },
    搜索: '*',
}