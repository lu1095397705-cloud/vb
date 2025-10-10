var rule={
    title:'樱花动漫',
    host:'https://www.857yhw.com/',
    // homeUrl:'/',
    url:'/type/fyclass-fypage.html',
    searchUrl: '/search/**----------fypage---.html',
    filterable:0,//是否启用分类筛选,
    searchable:2,//是否启用全局搜索,
    quickSearch:0,//是否启用快速搜索,   
    headers:{//网站的请求头,完整支持所有的,常带ua和cookies
        'User-Agent':'MOBILE_UA',
        // "Cookie": "searchneed=ok"
    }, 
    class_parse:'myui-header__menu nav-menu&&li;a&&Text;/(\\d+).html',
    class_exaclude:'动漫资讯',
    play_parse:true,
    lazy:"",
    limit:6,    
    推荐:'myui-vodlist__box;a&&title;img&&data-original;a&&href',
    一级:'.module-list&&.list-item;img&&alt;img&&data-original;a&&href',
    二级访问前:'',
    二级:{
        "title":".info-title&&Text",
        "img":".info-pic&&img&&data-original",
        "desc":".info-intro&&Text",
        "content":".info-short&&Text;.info-tag:eq(0)&&Text;.info-tag:eq(1)&&Text;.info-tag:eq(2)&&Text",
        "tabs":".tab-item",
        "lists":".playlist&&ul"
    },
    搜索:'*',
}
