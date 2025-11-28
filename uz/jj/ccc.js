import

{Crypto, load, _}
from

'assets://js/lib/cat.js';

let
key = 'sunnafh';
let
HOST = 'https://www.sunnafh.com';
let
siteKey = '';
let
siteType = 0;

const
UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1';

// 辅助函数：提取字符串中间内容
function
formatUrl(url)
{
if (url.indexOf('http') === 0)
return url;
return HOST + url;
}

// 辅助函数：简单的正则匹配
function
getStrByRegex(str, regex, group)
{
try {
let match = str.match(regex);
if (match & & match.length > group) {
return match[group];
}
} catch(e)
{}
return "";
}

let
spider = {
init: function(ext)
{
    console.log("初始化阳光电影JS爬虫");
},

home: function(filter)
{
// 手动定义分类，比网络请求更快
let
classes = [
    {type_id: '1', type_name: '电影'},
    {type_id: '2', type_name: '连续剧'},
    {type_id: '3', type_name: '综艺'},
    {type_id: '4', type_name: '动漫'}
];

return JSON.stringify({


class: classes,


filters: {}
});
},

homeVod: function(tid, page, filter, extend)
{
// 拼接URL: https: // www.sunnafh.com / vodshow / 1 - -------2 - --.html
let
input = HOST + '/vodshow/' + tid + '--------' + page + '---.html';

// 发起请求(req
是
UZVideo
环境内置方法)
let
html = req(input, {headers: {'User-Agent': UA}}).content;

let
list = [];
// 正则匹配列表页(适配
MXPro
模板)
// 匹配 < div


class ="module-item-pic" >...< a href="..." >...< img data-src="..." >...< / div >

// 注意：正则需要根据网页源码微调
const
regexStr = /

class ="module-item-pic"[\s\S] * ?href="(.*?)"[\s\S] * ?title="(.*?)"[\s\S] * ?data-src="(.*?)"[\s\S] * ?module-item-text">(.*?)<\/div>/g;


let
match;
while ((match = regexStr.exec(html)) !== null) {
list.push({
vod_id: match[1], // 使用链接作为ID
vod_name: match[2],
vod_pic: match[3],
vod_remarks: match[4]
});
}

return JSON.stringify({
    list: list
});
},

detail: function(ids)
{
let
url = formatUrl(ids);
let
html = req(url, {headers: {'User-Agent': UA}}).content;

let
vod = {
    vod_id: ids,
    vod_name: '',
    vod_pic: '',
    type_name: '',
    vod_year: '',
    vod_area: '',
    vod_content: '',
    vod_director: '',
    vod_actor: '',
    vod_play_from: '',
    vod_play_url: ''
};

// 正则提取详情信息
vod.vod_name = getStrByRegex(html, / < h1


class ="page-title" > (.* ?) < \ / h1 > /, 1);
vod.vod_pic = getStrByRegex(html, / class ="mobile-play"[\s\S] * ?data-src="(.*?)" /, 1);
vod.vod_content = getStrByRegex(html, / < meta name="description" content="(.*?)" /, 1);

// 提取播放列表
// 1. 提取线路名称 (Tab)
let playFrom =[];
const tabRegex = / data-dropdown-value="(.+?)" / g;
let tabMatch;
// 很多站点的 Tab 在


class ="module-tab-item" 里


const
tabAreaRegex = /

class ="module-tab-items-box"([\s\S] * ?) < \ / div > /;


let
tabArea = getStrByRegex(html, tabAreaRegex, 1);
if (tabArea) {
const tabNameRegex = / < span > (.* ?) < \ / span > / g;
let tnMatch;
while ((tnMatch = tabNameRegex.exec(tabArea)) !== null) {
// 简单清洗一下线路名
playFrom.push(tnMatch[1].replace( / & nbsp; / g, '').trim());
}
}

// 如果上面没取到，兜底尝试
if (playFrom.length === 0)
playFrom = ['默认线路'];
vod.vod_play_from = playFrom.join('$$$');

// 2.
提取播放地址
let
playUrl = [];
// 提取所有
list
容器
const
listAreaRegex = /

class ="module-play-list-content"([\s\S] * ?) < \ / div > / g;


let
listMatch;
while ((listMatch = listAreaRegex.exec(html)) !== null) {
let oneListStr = listMatch[1];
let oneListUrls =[];
// 提取单集链接
const linkRegex = / href="(.*?)"[\s\S] * ? < span > (.* ?) < \ / span > / g;
let linkMatch;
while ((linkMatch = linkRegex.exec(oneListStr)) !== null) {
let u = formatUrl(linkMatch[1]);
let n = linkMatch[2];
oneListUrls.push(n + '$' + u);
}
playUrl.push(oneListUrls.join('#'));
}

vod.vod_play_url = playUrl.join('$$$');

return JSON.stringify({
    list: [vod]
});
},

search: function(key, quick)
{
// 阳光电影搜索URL: / vodsearch / ------------- /?wd = 关键词
let
url = HOST + '/vodsearch/-------------/?wd=' + encodeURIComponent(key);
let
html = req(url, {headers: {'User-Agent': UA}}).content;

let
list = [];
// 搜索结果列表正则(通常和首页略有不同，或者结构类似)
// 假设结构为.module - search - item
const
regexStr = /

class ="module-search-item" >[\s\S] * ?href="(.*?)"[\s\S] * ?alt="(.*?)"[\s\S] * ?data-src="(.*?)"[\s\S] * ?video-serial">(.*?)<\/a>/g;


let
match;
while ((match = regexStr.exec(html)) !== null) {
list.push({
vod_id: match[1],
vod_name: match[2],
vod_pic: match[3],
vod_remarks: match[4]
});
}

return JSON.stringify({
    list: list
});
},

play: function(flag, id, flags)
{
// 阳光电影通常不需要二次解析，直接开启
Web
嗅探
// 1 = 嗅探, 0 = 直接播放
return JSON.stringify({
    parse: 1,
    url: id,
    header: {
        'User-Agent': UA
    }
});
}
};

export
default
spider;
