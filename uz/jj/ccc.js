
// ignore
// UZVideo 阳光电影
// 适配机制：利用 // ignore 屏蔽 export 语句

var HOST = 'https://www.sunnafh.com';
var MOBILE_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1';

// ---------------- 辅助函数 ----------------
function formatUrl(url) {
    if (!url) return "";
    if (url.indexOf('http') === 0) return url;
    if (url.indexOf('//') === 0) return 'https:' + url;
    return HOST + url;
}

function getStr(html, regex, index) {
    try {
        var m = html.match(regex);
        if (m && m.length > index) return m[index];
    } catch (e) {}
    return "";
}
// ----------------------------------------

var spider = {
    init: function (ext) {
        console.log("Sunnafh Init");
    },

    home: function (filter) {
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
        var url = HOST + '/vodshow/' + tid + '--------' + page + '---.html';

        // 使用 UZVideo 内置 req
        var res = req(url, {
            headers: { 'User-Agent': MOBILE_UA }
        });
        var html = res.content || "";
        var list = [];

        // 列表正则
        var regex = /<a[\s\S]*?href="(.*?)"[\s\S]*?title="(.*?)"[\s\S]*?data-src="(.*?)"[\s\S]*?class="module-poster-item/g;
        // 备用正则
        if (html.indexOf('module-item-pic') !== -1) {
            regex = /class="module-item-pic"[\s\S]*?href="(.*?)"[\s\S]*?title="(.*?)"[\s\S]*?data-src="(.*?)"[\s\S]*?module-item-text">(.*?)<\/div>/g;
        }

        var match;
        while ((match = regex.exec(html)) !== null) {
            list.push({
                vod_id: match[1],
                vod_name: match[2],
                vod_pic: formatUrl(match[3]),
                vod_remarks: match[4] || ""
            });
        }
        return JSON.stringify({ list: list });
    },

    detail: function (ids) {
        var url = formatUrl(ids);
        var res = req(url, {
            headers: { 'User-Agent': MOBILE_UA }
        });
        var html = res.content || "";

        var vod = {
            vod_id: ids,
            vod_name: getStr(html, /<h1 class="page-title">(.*?)<\/h1>/, 1),
            vod_pic: getStr(html, /class="mobile-play"[\s\S]*?data-src="(.*?)"/, 1),
            vod_content: getStr(html, /name="description" content="(.*?)"/, 1),
            vod_play_from: '',
            vod_play_url: ''
        };

        // 获取线路
        var playFrom = [];
        var tabRegex = /data-dropdown-value="(.+?)"/g;
        var tabMatch;
        while ((tabMatch = tabRegex.exec(html)) !== null) {
            playFrom.push(tabMatch[1]);
        }
        if (playFrom.length === 0) {
             var tabBox = getStr(html, /class="module-tab-items-box"([\s\S]*?)<\/div>/, 1);
             if (tabBox) {
                 var subRegex = /<span>(.*?)<\/span>/g;
                 var subMatch;
                 while ((subMatch = subRegex.exec(tabBox)) !== null) {
                     playFrom.push(subMatch[1]);
                 }
             }
        }
        if (playFrom.length === 0) playFrom = ['默认线路'];
        vod.vod_play_from = playFrom.join('$$$');

        // 获取播放列表
        var playUrl = [];
        var listRegex = /class="module-play-list-content"([\s\S]*?)<\/div>/g;
        var listMatch;
        while ((listMatch = listRegex.exec(html)) !== null) {
            var listHtml = listMatch[1];
            var urls = [];
            var linkRegex = /href="(.*?)"[\s\S]*?<span>(.*?)<\/span>/g;
            var linkMatch;
            while ((linkMatch = linkRegex.exec(listHtml)) !== null) {
                urls.push(linkMatch[2] + '$' + formatUrl(linkMatch[1]));
            }
            playUrl.push(urls.join('#'));
        }
        vod.vod_play_url = playUrl.join('$$$');

        return JSON.stringify({ list: [vod] });
    },

    search: function (key, quick) {
        var url = HOST + '/vodsearch/-------------/?wd=' + encodeURIComponent(key);
        var res = req(url, {
            headers: { 'User-Agent': MOBILE_UA }
        });
        var html = res.content || "";
        var list = [];
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
        return JSON.stringify({ list: list });
    },

    play: function (flag, id, flags) {
        return JSON.stringify({
            parse: 1,
            url: id,
            header: { 'User-Agent': MOBILE_UA }
        });
    }
};

// ignore
export default spider;
// ignore
