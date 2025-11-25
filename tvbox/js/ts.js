// 至臻影视源 - 适配TVBox的JavaScript版本
(function() {
    const sourceName = "至臻影视";
    const baseUrl = "https://www.miqk.cc";
    const timeout = 15000;

    // 工具函数
    function completeUrl(url) {
        if (!url) return '';
        if (url.startsWith('http')) return url;
        if (url.startsWith('//')) return 'https:' + url;
        if (url.startsWith('/')) return baseUrl + url;
        return baseUrl + '/' + url;
    }

    function encodeUrl(str) {
        return encodeURIComponent(str).replace(/%20/g, '+');
    }

    function log(message) {
        console.log(`[${sourceName}] ${message}`);
    }

    // 请求函数
    function request(url, options = {}) {
        const headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': baseUrl,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        };

        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();
            xhr.timeout = timeout;
            xhr.open('GET', url, true);

            // 设置请求头
            for (let key in headers) {
                xhr.setRequestHeader(key, headers[key]);
            }

            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4) {
                    if (xhr.status === 200) {
                        resolve(xhr.responseText);
                    } else {
                        reject(new Error(`HTTP ${xhr.status}: ${xhr.statusText}`));
                    }
                }
            };

            xhr.ontimeout = function() {
                reject(new Error('请求超时'));
            };

            xhr.onerror = function() {
                reject(new Error('网络错误'));
            };

            xhr.send();
        });
    }

    // 解析HTML的工具函数
    function parseHtml(html) {
        const parser = new DOMParser();
        return parser.parseFromString(html, 'text/html');
    }

    function extractText(element, selector) {
        if (!element) return '';
        const elem = element.querySelector(selector);
        return elem ? elem.textContent.trim() : '';
    }

    function extractAttr(element, selector, attr) {
        if (!element) return '';
        const elem = element.querySelector(selector);
        return elem ? elem.getAttribute(attr) || '' : '';
    }

    // TVBox标准接口函数
    function home() {
        log('加载首页');

        const classes = [
            {"type_id": "26", "type_name": "臻彩严选"},
            {"type_id": "1", "type_name": "至臻电影"},
            {"type_id": "2", "type_name": "至臻剧集"},
            {"type_id": "3", "type_name": "至臻动漫"},
            {"type_id": "4", "type_name": "至臻综艺"},
            {"type_id": "5", "type_name": "短剧吃到饱"},
            {"type_id": "24", "type_name": "老剧计划"}
        ];

        return JSON.stringify({
            class: classes,
            list: []
        });
    }

    function homeVod() {
        log('加载首页推荐视频');

        return new Promise((resolve) => {
            request(baseUrl)
                .then(html => {
                    const doc = parseHtml(html);
                    const videos = parseHomeVideos(doc);

                    resolve(JSON.stringify({
                        list: videos
                    }));
                })
                .catch(error => {
                    log(`首页推荐获取失败: ${error}`);
                    resolve(JSON.stringify({list: []}));
                });
        });
    }

    function parseHomeVideos(doc) {
        const videos = [];

        // 尝试多种选择器
        const selectors = [
            '.module-items .module-item',
            '.vod-list .vod-item',
            '.video-list .video-item',
            '.list-wrap .list-item',
            'a[href*="/vod/detail/"]'
        ];

        let elements = [];
        for (let selector of selectors) {
            elements = doc.querySelectorAll(selector);
            if (elements.length > 5) break;
        }

        elements.forEach((element, index) => {
            if (index >= 20) return; // 限制数量

            try {
                const video = parseVideoElement(element);
                if (video) videos.push(video);
            } catch (e) {
                log(`解析视频项失败: ${e}`);
            }
        });

        log(`解析到 ${videos.length} 个首页视频`);
        return videos;
    }

    function parseVideoElement(element) {
        let link, title, cover, remark;

        // 获取链接
        if (element.tagName === 'A') {
            link = element;
        } else {
            link = element.querySelector('a[href*="/vod/detail/"]');
        }

        if (!link || !link.href) return null;

        const href = link.getAttribute('href');
        if (!href || !href.includes('/vod/detail/')) return null;

        // 获取标题
        title = link.getAttribute('title') ||
               extractText(link, '.vod-name') ||
               extractText(link, '.title') ||
               link.textContent.trim();

        if (!title || title.length < 2) return null;

        // 获取封面
        const img = element.querySelector('img');
        if (img) {
            cover = img.getAttribute('data-src') || img.getAttribute('src');
        }

        // 获取备注
        remark = extractText(element, '.remarks') ||
                extractText(element, '.tag') ||
                extractText(element, '.score') ||
                '影视';

        return {
            vod_id: href,
            vod_name: title,
            vod_pic: completeUrl(cover),
            vod_remarks: remark
        };
    }

    function category(tid, pg, filter, extend) {
        log(`加载分类: ${tid}, 页码: ${pg}`);

        return new Promise((resolve) => {
            let url;
            if (parseInt(pg) === 1) {
                url = `${baseUrl}/index.php/vod/type/id/${tid}.html`;
            } else {
                url = `${baseUrl}/index.php/vod/type/id/${tid}/page/${pg}.html`;
            }

            request(url)
                .then(html => {
                    const doc = parseHtml(html);
                    const videos = parseCategoryVideos(doc);

                    resolve(JSON.stringify({
                        page: parseInt(pg),
                        pagecount: 999,
                        limit: videos.length,
                        total: videos.length * 20,
                        list: videos
                    }));
                })
                .catch(error => {
                    log(`分类获取失败: ${error}`);
                    resolve(JSON.stringify({
                        page: parseInt(pg),
                        pagecount: 1,
                        limit: 0,
                        total: 0,
                        list: []
                    }));
                });
        });
    }

    function parseCategoryVideos(doc) {
        const videos = [];
        const links = doc.querySelectorAll('a[href*="/vod/detail/"]');

        links.forEach(link => {
            try {
                const element = link.closest('.module-item, .vod-item, .video-item, li') || link.parentElement;
                const video = parseVideoElement(element || link);
                if (video) videos.push(video);
            } catch (e) {
                log(`解析分类视频失败: ${e}`);
            }
        });

        // 去重
        const seen = new Set();
        const uniqueVideos = videos.filter(video => {
            if (seen.has(video.vod_id)) return false;
            seen.add(video.vod_id);
            return true;
        });

        log(`解析到 ${uniqueVideos.length} 个分类视频`);
        return uniqueVideos;
    }

    function detail(id) {
        log(`加载详情: ${id}`);

        return new Promise((resolve) => {
            let url = id.startsWith('http') ? id : completeUrl(id);

            request(url)
                .then(html => {
                    const doc = parseHtml(html);
                    const detail = parseDetail(doc, id);

                    resolve(JSON.stringify({
                        list: detail ? [detail] : []
                    }));
                })
                .catch(error => {
                    log(`详情获取失败: ${error}`);
                    resolve(JSON.stringify({list: []}));
                });
        });
    }

    function parseDetail(doc, id) {
        try {
            const detail = {
                vod_id: id,
                vod_name: '',
                vod_pic: '',
                vod_content: '',
                vod_play_from: '播放线路',
                vod_play_url: ''
            };

            // 标题
            const title = doc.querySelector('title');
            if (title) {
                detail.vod_name = title.textContent.replace(' - 至臻影视', '').trim();
            }

            // 封面
            const img = doc.querySelector('img[src*=".jpg"], img[src*=".png"], img[src*=".webp"]');
            if (img) {
                detail.vod_pic = completeUrl(img.getAttribute('src'));
            }

            // 简介
            const contentSelectors = ['.content', '.intro', '.description', '.summary'];
            for (let selector of contentSelectors) {
                const elem = doc.querySelector(selector);
                if (elem) {
                    detail.vod_content = elem.textContent.trim();
                    break;
                }
            }

            // 播放链接
            const playLinks = extractPlayLinks(doc);
            if (playLinks.length > 0) {
                const playUrls = playLinks.map((link, index) => `第${index + 1}集$${link}`).join('#');
                detail.vod_play_url = playUrls;
            }

            log(`详情解析成功: ${detail.vod_name}`);
            return detail;

        } catch (error) {
            log(`详情解析失败: ${error}`);
            return null;
        }
    }

    function extractPlayLinks(doc) {
        const links = [];
        const text = doc.body.textContent;

        // 正则表达式匹配各种播放链接
        const patterns = [
            /https?:\/\/[^\s<>"']+\.(m3u8|mp4|avi|mkv|flv)/gi,
            /https?:\/\/pan\.baidu\.com\/s\/[\w-]+/gi,
            /https?:\/\/www\.aliyundrive\.com\/s\/[\w]+/gi,
            /https?:\/\/cloud\.189\.cn\/[\w\/]+/gi
        ];

        patterns.forEach(pattern => {
            const matches = text.match(pattern);
            if (matches) {
                links.push(...matches);
            }
        });

        // 去重
        const uniqueLinks = [...new Set(links)];
        log(`提取到 ${uniqueLinks.length} 个播放链接`);
        return uniqueLinks;
    }

    function search(wd, quick, pg) {
        log(`搜索: ${wd}, 页码: ${pg}`);

        return new Promise((resolve) => {
            const encodedWd = encodeUrl(wd);
            const url = `${baseUrl}/index.php/vod/search/page/${pg}/wd/${encodedWd}.html`;

            request(url)
                .then(html => {
                    const doc = parseHtml(html);
                    const videos = parseCategoryVideos(doc);

                    resolve(JSON.stringify({
                        page: parseInt(pg),
                        pagecount: 999,
                        limit: videos.length,
                        total: videos.length * 20,
                        list: videos
                    }));
                })
                .catch(error => {
                    log(`搜索失败: ${error}`);
                    resolve(JSON.stringify({
                        page: parseInt(pg),
                        pagecount: 1,
                        limit: 0,
                        total: 0,
                        list: []
                    }));
                });
        });
    }

    function play(flag, id, flags) {
        log(`播放: ${id}`);

        // 直接返回播放地址，不进行解析
        return JSON.stringify({
            parse: 0,
            url: id,
            header: JSON.stringify({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': baseUrl
            })
        });
    }

    // 导出函数供TVBox调用
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = {
            home: home,
            homeVod: homeVod,
            category: category,
            detail: detail,
            search: search,
            play: play
        };
    } else {
        // 浏览器环境测试
        window[sourceName] = {
            home: home,
            homeVod: homeVod,
            category: category,
            detail: detail,
            search: search,
            play: play
        };
    }

    log('至臻影视源加载完成');
})();