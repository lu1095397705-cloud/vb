// UZVideo 专用 - 阳光电影修正版
// 移除所有外部 import，使用纯原生写法

const HOST = 'https://www.sunnafh.com';
const MOBILE_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1';

// ---------------- 辅助函数开始 ----------------
// 格式化图片或链接地址
function formatUrl(url) {
    if (!url) return "";
    if (url.startsWith('http')) return url;
    if (url.startsWith('//')) return 'https:' + url;
    return HOST + url;
}

// 简单的正则匹配工具，防止报错
function matchOne(str, regex, index) {
    try {
        const m = str.match(regex);
        return (m && m.length > index) ? m[index] : "";
    } catch (e) {
        return "";
    }
}
// ---------------- 辅助函数结束 ----------------

// 定义爬虫对象
var spider = {
    init: function (ext) {
        console.log("Sunnafh Spider Init");
    },

    home: function (filter) {
        // 手动写死分类，最稳定
        var classes = [
            { type_id: '1', type_name: '电影' },
            { type_id: '2', type_name: '连续剧' },
            { type_id: '3', type_name: '综艺' },
            { type_id: '4', type_name: '动漫' }
        ];
        return JSON.stringify({
            class: classes
        });
    },

    homeVod: function (tid, page, filter, extend) {
        // 拼接 URL
        var url = HOST + '/vodshow/' + tid + '--------' + page + '---.html';

        // 发送请求
        var html = req(url, {
            headers: { 'User-Agent': MOBILE_UA }
        }).content;

        var list = [];
        // 针对 MXPro 模板的正则解析
        // 寻找 <a href="..." class="module-poster-item ...">
        // 注意：正则需要匹配换行符，JS中用 [\s\S]*?
        var regex = /<a[\s\S]*?href="(.*?)"[\s\S]*?title="(.*?)"[\s\S]*?data-src="(.*?)"[\s\S]*?class="module-poster-item/g;
        // 备用正则（有的模板结构不同）
        if (html.indexOf('module-item-pic') > -1) {
            regex = /class="module-item-pic"[\s\S]*?href="(.*?)"[\s\S]*?title="(.*?)"[\s\S]*?data-src="(.*?)"[\s\S]*?module-item-text">(.*?)<\/div>/g;
        }

        var match;
        while ((match = regex.exec(html)) !== null) {
            list.push({
                vod_id: match[1],
                vod_name: match[2],
                vod_pic: formatUrl(match[3]),
                vod_remarks: match[4] || ''
            });
        }

        return JSON.stringify({
            list: list
        });
    },

    detail: function (ids) {
        var url = formatUrl(ids);
        var html = req(url, {
            headers: { 'User-Agent': MOBILE_UA }
        }).content;

        var vod = {
            vod_id: ids,
            vod_name: matchOne(html, /<h1 class="page-title">(.*?)<\/h1>/, 1),
            vod_pic: matchOne(html, /class="mobile-play"[\s\S]*?data-src="(.*?)"/, 1),
            vod_type: '',
            vod_year: '',
            vod_area: '',
            vod_content: matchOne(html, /name="description" content="(.*?)"/, 1),
            vod_play_from: '',
            vod_play_url: ''
        };

        // --- 解析线路 (Tabs) ---
        var playFrom = [];
        // 匹配 <div class="module-tab-item ..."><span>线路名</span></div>
        var tabRegex = /data-dropdown-value="(.+?)"/g;
        var tabMatch;
        // 先尝试在 dropdown 里找
        while ((tabMatch = tabRegex.exec(html)) !== null) {
            playFrom.push(tabMatch[1]);
        }
        // 如果没找到，尝试在 module-tab-item 里找
        if (playFrom.length === 0) {
             var tabStr = matchOne(html, /class="module-tab-items-box"([\s\S]*?)<\/div>/, 1);
             var subTabRegex = /<span>(.*?)<\/span>/g;
             while ((tabMatch = subTabRegex.exec(tabStr)) !== null) {
                 playFrom.push(tabMatch[1]);
             }
        }
        if (playFrom.length === 0) playFrom = ['默认线路'];
        vod.vod_play_from = playFrom.join('$$$');

        // --- 解析播放列表 (Lists) ---
        var playUrl = [];
        var listAreaRegex = /class="module-play-list-content"([\s\S]*?)<\/div>/g;
        var listArea;
        while ((listArea = listAreaRegex.exec(html)) !== null) {
            var oneListStr = listArea[1];
            var oneUrlList = [];
            // 匹配 <a href="..."><span>集数</span></a>
            var linkRegex = /href="(.*?)"[\s\S]*?<span>(.*?)<\/span>/g;
            var linkMatch;
            while ((linkMatch = linkRegex.exec(oneListStr)) !== null) {
                var u = formatUrl(linkMatch[1]);
                var n = linkMatch[2];
                oneUrlList.push(n + '$' + u);
            }
            playUrl.push(oneUrlList.join('#'));
        }
        vod.vod_play_url = playUrl.join('$$$');

        return JSON.stringify({
            list: [vod]
        });
    },

    search: function (key, quick) {
        var url = HOST + '/vodsearch/-------------/?wd=' + encodeURIComponent(key);
        var html = req(url, {
            headers: { 'User-Agent': MOBILE_UA }
        }).content;

        var list = [];
        // 搜索结果正则
        var regex = /class="module-search-item">[\s\S]*?href="(.*?)"[\s\S]*?alt="(.*?)"[\s\S]*?data-src="(.*?)"[\s\S]*?video-serial">(.*?)<\/a>/g;
        var match;
        while ((match = regex.exec(html)) !== null) {
            list.push({
                vod_id: match[1],
                vod_name: match[2],
                vod_pic: formatUrl(match[3]),
                vod_remarks: match[4]
            });
        }

        return JSON.stringify({
            list: list
        });
    },

    play: function (flag, id, flags) {
        return JSON.stringify({
            parse: 1, // 开启嗅探
            url: id,
            header: {
                'User-Agent': MOBILE_UA
            }
        });
    }
};

export default spider;
