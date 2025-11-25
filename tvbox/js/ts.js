var rule = {
    title: '至臻影视',
    host: 'https://www.miqk.cc',
    homeUrl: '/',
    url: '/index.php/vod/type/id/fyclass/page/fypage.html',
    searchUrl: '/index.php/vod/search/page/fypage/wd/**.html',
    detailUrl: '/vod/detail/id/fyid.html',
    headers: {
        'User-Agent': 'MOBILE_UA'
    },
    timeout: 5000,
    class_name: '臻彩严选&至臻电影&至臻剧集&至臻动漫&至臻综艺&短剧吃到饱&老剧计划',
    class_url: '26&1&2&3&4&5&24',

    // 首页推荐
    homeUrl: '/',
    homeVod: function() {
        var html = request(this.host);
        var list = [];

        try {
            // 解析首页推荐视频
            var items = parseDom(html, 'a[href*="/vod/detail/"]');
            for (var i = 0; i < Math.min(items.length, 20); i++) {
                var item = items[i];
                var href = item.attr('href');
                var title = item.attr('title') || item.text();
                var img = item.find('img').attr('src') || '';

                if (href && title) {
                    list.push({
                        vod_id: href,
                        vod_name: title,
                        vod_pic: this.joinUrl(img),
                        vod_remarks: ''
                    });
                }
            }
        } catch (e) {
            console.log('解析首页推荐失败: ' + e);
        }

        return list;
    },

    // 分类页面
    cateUrl: function(fyclass, fypage) {
        return this.host + '/index.php/vod/type/id/' + fyclass + '/page/' + fypage + '.html';
    },

    // 分类数据解析
    category: function(fyclass, fypage, filter, extend) {
        var url = this.cateUrl(fyclass, fypage);
        var html = request(url);
        var list = [];

        try {
            var items = parseDom(html, 'a[href*="/vod/detail/"]');
            for (var i = 0; i < items.length; i++) {
                var item = items[i];
                var href = item.attr('href');
                var title = item.attr('title') || item.text();
                var img = item.find('img').attr('src') || '';

                if (href && title) {
                    list.push({
                        vod_id: href,
                        vod_name: title,
                        vod_pic: this.joinUrl(img),
                        vod_remarks: this.getRemarks(item)
                    });
                }
            }
        } catch (e) {
            console.log('解析分类失败: ' + e);
        }

        return {
            list: list,
            page: fypage,
            pagecount: 999,
            limit: list.length,
            total: list.length * 20
        };
    },

    // 详情页面
    detail: function(vod_id) {
        var url = vod_id.startsWith('http') ? vod_id : this.host + vod_id;
        var html = request(url);
        var detail = {};

        try {
            // 解析标题
            var title = parseDom(html, 'title').text();
            detail.vod_name = title.replace(' - 至臻影视', '');

            // 解析封面
            var img = parseDom(html, 'img').attr('src');
            detail.vod_pic = this.joinUrl(img);

            // 解析简介
            var content = parseDom(html, '.content, .intro, .description').text();
            detail.vod_content = content || '暂无简介';

            // 解析播放地址
            var playList = this.parsePlayLinks(html);
            detail.vod_play_from = playList.map(function(item) { return item.name; }).join('$$$');
            detail.vod_play_url = playList.map(function(item) {
                return item.urls.map(function(url, idx) {
                    return '第' + (idx + 1) + '集$' + url;
                }).join('#');
            }).join('$$$');

        } catch (e) {
            console.log('解析详情失败: ' + e);
        }

        return {
            list: [detail]
        };
    },

    // 搜索
    search: function(wd, quick, pg) {
        var url = this.host + '/index.php/vod/search/page/' + pg + '/wd/' + encodeURIComponent(wd) + '.html';
        var html = request(url);
        var list = [];

        try {
            var items = parseDom(html, 'a[href*="/vod/detail/"]');
            for (var i = 0; i < items.length; i++) {
                var item = items[i];
                var href = item.attr('href');
                var title = item.attr('title') || item.text();

                if (href && title) {
                    list.push({
                        vod_id: href,
                        vod_name: title,
                        vod_pic: '',
                        vod_remarks: ''
                    });
                }
            }
        } catch (e) {
            console.log('搜索失败: ' + e);
        }

        return {
            list: list,
            page: pg,
            pagecount: 999,
            limit: list.length,
            total: list.length * 20
        };
    },

    // 播放
    play: function(flag, id, flags) {
        return {
            parse: 0,
            url: id,
            header: JSON.stringify(this.headers)
        };
    },

    // 工具函数
    joinUrl: function(url) {
        if (!url) return '';
        if (url.startsWith('http')) return url;
        if (url.startsWith('//')) return 'https:' + url;
        if (url.startsWith('/')) return this.host + url;
        return this.host + '/' + url;
    },

    getRemarks: function(item) {
        var remarks = item.find('.remarks, .tag, .score').text();
        return remarks || '影视';
    },

    parsePlayLinks: function(html) {
        var playList = [];
        var urls = [];

        // 匹配m3u8链接
        var m3u8Matches = html.match(/https?:\/\/[^\s<>"']+\.m3u8[^\s<>"']*/g) || [];
        // 匹配mp4链接
        var mp4Matches = html.match(/https?:\/\/[^\s<>"']+\.mp4[^\s<>"']*/g) || [];
        // 匹配网盘链接
        var panMatches = html.match(/https?:\/\/pan\.baidu\.com\/s\/[^\s<>"']*/g) || [];

        urls = urls.concat(m3u8Matches, mp4Matches, panMatches);

        if (urls.length > 0) {
            playList.push({
                name: '播放线路',
                urls: urls
            });
        }

        return playList;
    }
};

// TVBox标准接口导出
function home() {
    return JSON.stringify(rule.homeVod());
}

function homeVod() {
    return JSON.stringify({list: rule.homeVod()});
}

function category(tid, pg, filter, extend) {
    return JSON.stringify(rule.category(tid, pg, filter, extend));
}

function detail(id) {
    return JSON.stringify(rule.detail(id));
}

function search(wd, quick, pg) {
    return JSON.stringify(rule.search(wd, quick, pg));
}

function play(flag, id, flags) {
    return JSON.stringify(rule.play(flag, id, flags));
}