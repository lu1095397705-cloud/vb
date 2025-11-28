// ignore
// @name:888
// 该扩展依赖 uz3lib.js 中的 cheerio 库
// ignore

class SunnaFHAdapter extends WebApiBase {
    constructor() {
        super();
        this.webSite = "https://www.sunnafh.com";
        this.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Referer": this.webSite
        };
    }

    /**
     * 辅助方法：处理请求
     * uz 环境通常提供 req 方法
     */
    async request(url) {
        try {
            // 假设 uz 环境提供了 req(url, options) 方法，返回 { content: string }
            // 如果是其他 HTTP 库，请在此处适配
            let res = await req(url, {
                headers: this.headers
            });
            return res.content;
        } catch (e) {
            console.error("Request Error:", e);
            return "";
        }
    }

    /**
     * 获取分类列表 (流程 A -> A1)
     * @returns {Promise<RepVideoClassList>}
     */
    async getClassList() {
        const html = await this.request(this.webSite);
        const $ = cheerio.load(html);
        const json = {
            data: []
        };

        // 解析导航栏，根据实际网站结构调整选择器
        // 通常在 .nav-menu 或 .navbar 下
        // SunnaFH 似乎使用的是典型的模板
        $('.nav-menu > li > a').each((index, element) => {
            const name = $(element).attr('title') || $(element).text().trim();
            const href = $(element).attr('href');

            // 忽略首页和空链接
            if (href && href !== '/' && href !== '#' && !href.includes('http')) {
                // 从 /vodtype/1.html 中提取 ID
                const match = href.match(/\/vodtype\/(\d+)\.html/);
                if (match) {
                    const typeId = match[1];
                    json.data.push({
                        type_id: typeId,
                        type_name: name,
                        hasSubclass: false // 设为 false 直接走 getVideoList，简化流程
                    });
                }
            }
        });

        return JSON.stringify(json);
    }

    /**
     * 获取二级分类 (流程 B -> C)
     * 当前 hasSubclass 为 false，此方法可能不会被频繁调用，但需保留
     */
    async getSubclassList(classId) {
        // 如果需要筛选功能，在此实现
        return JSON.stringify({
            data: []
        });
    }

    /**
     * 获取二级分类视频列表 (流程 C -> C1)
     */
    async getSubclassVideoList(classId, page, filter) {
        return this.getVideoList(classId, page);
    }

    /**
     * 获取视频列表 (流程 B -> D)
     * @param {string} classId 分类ID
     * @param {number} page 页码
     * @returns {Promise<RepVideoList>}
     */
    async getVideoList(classId, page) {
        // 构造 URL: https://www.sunnafh.com/vodtype/{id}-{page}.html
        const url = `${this.webSite}/vodtype/${classId}-${page}.html`;
        const html = await this.request(url);
        const $ = cheerio.load(html);
        const json = {
            data: []
        };

        // 解析视频列表，常见选择器 .module-item
        $('.module-item').each((index, element) => {
            const $item = $(element);
            const $link = $item.find('.module-item-cover .module-item-pic > a');
            const $img = $item.find('.module-item-cover .module-item-pic > img');
            const $title = $item.find('.module-item-title');
            const $note = $item.find('.module-item-text'); // 更新状态，如 "更新至10集"

            const href = $link.attr('href');
            const title = $link.attr('title') || $title.text().trim();
            // 尝试获取 data-original 或 src
            const cover = $img.attr('data-original') || $img.attr('src');
            const remark = $note.text().trim();

            if (href) {
                // 从 /voddetail/123.html 提取 ID
                // 有些网站列表页链接是 detail，有些直接是 play，通常是 detail
                const idMatch = href.match(/\/voddetail\/(\d+)\.html/);
                if (idMatch) {
                    json.data.push({
                        vod_id: idMatch[1],
                        vod_name: title,
                        vod_pic: cover,
                        vod_remarks: remark
                    });
                }
            }
        });

        return JSON.stringify(json);
    }

    /**
     * 获取视频详情 (流程 E)
     * @param {string} vodId 视频ID
     * @returns {Promise<RepVideoDetail>}
     */
    async getVideoDetail(vodId) {
        const url = `${this.webSite}/voddetail/${vodId}.html`;
        const html = await this.request(url);
        const $ = cheerio.load(html);

        const vod_name = $('h1.page-title').text().trim();
        const vod_pic = $('.mobile-play').find('img').attr('data-original') || $('.mobile-play').find('img').attr('src');
        const vod_content = $('.video-info-content span').text().trim(); // 简介
        const vod_actor = $('.video-info-actor').text().trim();
        const vod_director = $('.video-info-items:contains("导演")').text().replace("导演：", "").trim();

        // 解析播放线路
        const vod_play_from = [];
        const vod_play_url = [];

        // 获取线路名称 tab
        $('.module-tab-item').each((i, el) => {
            const fromName = $(el).attr('data-dropdown-value') || $(el).text().trim();
            vod_play_from.push(fromName);
        });

        // 获取每一组线路的集数列表
        $('.module-play-list').each((i, el) => {
            let urls = [];
            $(el).find('a').each((j, subEl) => {
                const epName = $(subEl).text().trim();
                const epHref = $(subEl).attr('href');
                if (epHref) {
                    // 格式：名称$URL (URL 这里通常是 web 路径，之后在 getVideoPlayUrl 解析)
                    urls.push(`${epName}$${epHref}`);
                }
            });
            vod_play_url.push(urls.join('#'));
        });

        const json = {
            data: {
                vod_id: vodId,
                vod_name: vod_name,
                vod_pic: vod_pic,
                vod_actor: vod_actor,
                vod_director: vod_director,
                vod_content: vod_content,
                vod_play_from: vod_play_from.join('$$$'),
                vod_play_url: vod_play_url.join('$$$')
            }
        };

        return JSON.stringify(json);
    }

    /**
     * 获取播放链接 (流程 F)
     * @param {string} playUrl 上一步返回的 url (例如 /vodplay/123-1-1.html)
     * @returns {Promise<RepVideoPlayUrl>}
     */
    async getVideoPlayUrl(playUrl) {
        // 如果传入的已经是 http 开头的链接（虽然少见），直接返回
        if (playUrl.startsWith('http')) {
            return JSON.stringify({
                headers: this.headers,
                url: playUrl
            });
        }

        const targetUrl = this.webSite + playUrl;
        const html = await this.request(targetUrl);

        // 解析播放页
        // 通常这类网站会将播放信息放在一个 player_aaaa 变量中
        let realUrl = "";

        try {
            // 匹配 <script> 中的 JSON 数据
            const jsonMatch = html.match(/player_aaaa\s*=\s*({.*?});/);
            if (jsonMatch && jsonMatch[1]) {
                const playerData = JSON.parse(jsonMatch[1]);
                realUrl = playerData.url;
            } else {
                // 备用正则，匹配 "url":"..."
                const urlMatch = html.match(/"url"\s*:\s*"(.*?)"/);
                if (urlMatch) {
                    realUrl = urlMatch[1];
                }
            }
        } catch (e) {
            console.error("Parse Play URL Error", e);
        }

        // 处理 URL 解码（有些可能是 escape 编码的）
        if (realUrl) {
            // 简单的解码尝试
            realUrl = decodeURIComponent(realUrl);
        }

        return JSON.stringify({
            headers: {
                "User-Agent": this.headers["User-Agent"],
                "Referer": targetUrl // 播放时通常需要引用页 Referer
            },
            url: realUrl
        });
    }

    /**
     * 搜索视频 (流程 S -> S1)
     * @param {string} searchKey 搜索关键词
     * @returns {Promise<RepVideoList>}
     */
    async searchVideo(searchKey) {
        // 构造搜索 URL: https://www.sunnafh.com/vodsearch/-------------/?wd=key
        // 或者 /vodsearch.html?wd=key
        const url = `${this.webSite}/vodsearch/-------------/.html?wd=${encodeURIComponent(searchKey)}`;
        const html = await this.request(url);
        const $ = cheerio.load(html);
        const json = {
            data: []
        };

        // 搜索结果列表结构通常和分类列表类似，或者稍微不同（.module-search-item）
        // 假设是 .module-search-item
        $('.module-search-item').each((index, element) => {
            const $item = $(element);
            const $link = $item.find('.video-serial'); // 或者是 .video-cover a
            const $img = $item.find('.module-item-pic img');
            const $title = $item.find('.video-info-header h3 a');

            // 兼容性获取
            let href = $title.attr('href') || $item.find('a').attr('href');
            let title = $title.text().trim();
            let cover = $img.attr('data-original') || $img.attr('src');
            let remark = $item.find('.video-serial').text().trim();

            if (href) {
                const idMatch = href.match(/\/voddetail\/(\d+)\.html/);
                if (idMatch) {
                    json.data.push({
                        vod_id: idMatch[1],
                        vod_name: title,
                        vod_pic: cover,
                        vod_remarks: remark
                    });
                }
            }
        });

        // 如果搜索结构和普通列表一样是 .module-item
        if (json.data.length === 0) {
            $('.module-item').each((index, element) => {
                const $item = $(element);
                const $link = $item.find('.module-item-cover .module-item-pic > a');
                const $img = $item.find('.module-item-cover .module-item-pic > img');
                const $title = $item.find('.module-item-title');
                const $note = $item.find('.module-item-text');

                const href = $link.attr('href');
                const title = $link.attr('title') || $title.text().trim();
                const cover = $img.attr('data-original') || $img.attr('src');
                const remark = $note.text().trim();

                if (href) {
                    const idMatch = href.match(/\/voddetail\/(\d+)\.html/);
                    if (idMatch) {
                        json.data.push({
                            vod_id: idMatch[1],
                            vod_name: title,
                            vod_pic: cover,
                            vod_remarks: remark
                        });
                    }
                }
            });
        }

        return JSON.stringify(json);
    }
}
