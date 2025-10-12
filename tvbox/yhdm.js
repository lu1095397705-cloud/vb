var rule={
    title: '穷次元',
    host: 'https://jciyuan.com',
    // homeUrl:'/',
    url: '/show/fyclassfyfilter.html',
    searchUrl: '/acgsearch/**-------------.html',
    searchable: 2,
    quickSearch: 0,
    filterable: 1,
    headers: {//网站的请求头,完整支持所有的,常带ua和cookies
        'User-Agent': 'MOBILE_UA',
        // "Cookie": "searchneed=ok"
    },
    class_parse: '.navbar&&div&&ul&&li;a&&title;a&&href;.*/(.*?).html',
    cate_exclude: '解析|动态',
    play_parse: true,
    lazy: '',
    limit: 6,
    推荐: '.module-items;a&&title;img&&data-original;a&&href',
    一级: '.module-item-cover;a&&Text;a&&href;img&&data-original',
    二级: {
        "title": "h1&&Text",
        "img": ".module-info-pic&&img&&data-original",
        "desc": ".module-info-introduction&&Text",
        "content": ".module-info-item:eq(0)&&Text;.module-info-item:eq(1)&&Text;.module-info-item:eq(2)&&Text",
        "tabs": ".module-tab-item",
        "lists": ".module-list:eq(#id)&&li"
    },
    搜索: '.module-item-cover;a&&Text;a&&href;img&&data-original',
    

    
   
}
