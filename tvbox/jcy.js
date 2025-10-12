//https://jciyuan.com/
var rule = {
    title: '囧次元',
    host: 'https://jciyuan.com',
    //homeUrl: '/acgshow/fyclass-----------.html',
    url: '/acgshow/fyclass--------fypage---.html',
    filterable: 0, //是否启用分类筛选,
    //filter_url: '--{{fl.by}}-{{fl.class}}--{{fl.letter}}---fypage---{{fl.year}}',
    searchUrl: '/search/**----------fypage---.html',
    searchable: 2, //是否启用全局搜索,
    quickSearch: 0, //是否启用快速搜索,
    headers: { //网站的请求头,完整支持所有的,常带ua和cookies
        'User-Agent': 'MOBILE_UA',
    },
    class_parse: '.swiper-slide navbar-item;a&&title;a&&href;.*/(\\w+).html',
    play_parse: true,
    detailUrl: '',
    lazy: "",
    limit: 6,
    推荐: '*',
    一级: '.blockcontent1&&.blockdif2;img&&alt;img&&src;.newname&&Text;a&&href',//列表；名称；图片，剧集数；链接,
    二级访问前: '',
    二级: {
        "title": ".detail_imform_name&&Text;detail_imform_value:eq(0)&&Text",//名称；状态
        "img": ".poster&&src",
        "desc": ".detail_imform_kv:eq(0)&&Text;.detail_imform_value:eq(5)&&Text;.detail_imform_value:eq(2)&&Text;.detail_imform_kv:eq(0)&&Text;.detail_imform_kv:eq(3)&&Text",
        "content": ".detail_imform_desc_pre&&Text",//简介
        "tabs": "#menu0&&li",//线路名
        "lists": ".movurl:eq(#id)&&li"//列表
    },
    搜索: '*',
}