// http://www.ntdm.tv
var rule = {
    title: 'NT动漫',
    host: 'http://www.ntdm8.com',
    homeUrl: '/type/riben.html',
    // url:'/show/fyclass--------fypage---.html',
    url: '/show/fyclassfyfilter.html',
    filterable: 1, //是否启用分类筛选,
    filter_url: '--{{fl.by}}-{{fl.class}}--{{fl.letter}}---fypage---{{fl.year}}',
   
    searchUrl: '/search/**----------fypage---.html',
    searchable: 2, //是否启用全局搜索,
    quickSearch: 0, //是否启用快速搜索,
    headers: { //网站的请求头,完整支持所有的,常带ua和cookies
        'User-Agent': 'MOBILE_UA',
    },
    class_parse: '.search-tag li;a&&Text;a&&href;.*/(\\w+).html',
    play_parse: true,
    detailUrl: '',
    lazy: "",
    limit: 6,
    推荐: '*',
    一级: '.blockcontent1&&.blockdif2;img&&alt;img&&src;.newname&&Text;a&&href',
    二级访问前: '',
    二级: {
        "title": "h4&&Text;.detail_imform_value:eq(6)&&Text",
        "img": ".poster&&src",
        "desc": ".detail_imform_kv:eq(0)&&Text;.detail_imform_value:eq(5)&&Text;.detail_imform_value:eq(2)&&Text;.detail_imform_kv:eq(0)&&Text;.detail_imform_kv:eq(3)&&Text",
        "content": ".detail_imform_desc_pre&&Text",
        "tabs": "#menu0&&li",
        "lists": ".movurl:eq(#id)&&li"
    },
    搜索: '*',
}