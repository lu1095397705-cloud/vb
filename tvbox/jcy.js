//https://jciyuan.com/
var rule = {
    title: '囧次元',
    host: 'https://jciyuan.com',
    homeUrl: '/acgshow/fyclass-----------.html',
    url: '/acgshow/fyclass--------fypage---.html',
    filterable: 0, //是否启用分类筛选,
    //filter_url: '--{{fl.by}}-{{fl.class}}--{{fl.letter}}---fypage---{{fl.year}}',
    searchUrl: '/search/**----------fypage---.html',
    searchable: 2, //是否启用全局搜索,
    quickSearch: 0, //是否启用快速搜索,
    headers: { //网站的请求头,完整支持所有的,常带ua和cookies
        'User-Agent': 'MOBILE_UA',
    },
    class_parse: '.navbar&&ul&&li;a&&title;a&&href;.*/(\\w+).html',
    cate_exclude: '追剧周表|热榜|APP',
    play_parse: true,
    detailUrl: '',
    lazy: "",
    limit: 6,
    推荐: '*',
    一级: '.module-items;img&&alt;img&&data-original;.module-item-note&&Text;a&&href',//列表；名称；图片，剧集数；链接,
    二级访问前: '',
    二级: {
        "title": ".h1&&Text;.module-info-item-content&&Text",//名称；状态
        "img": ".module-item-pic&&src",
        "content": "",//简介
        "tabs": ".data-dropdown-value",//线路名
        "lists": "#panel1:eq(#id)&&a"//列表
    },
    搜索: '*',
}