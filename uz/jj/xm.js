//@name:小米影视
//@version:1.0.2
//@webSite:http://xiaomi666.fun
//@remark:适配Maccms通用/MxPro模板，增强播放解析
//@order: A01
const appConfig = {
    _webSite: 'http://xiaomi666.fun',
    get webSite() {
        return this._webSite
    },
    set webSite(value) {
        this._webSite = value
    },
    _uzTag: '',
    get uzTag() {
        return this._uzTag
    },
    set uzTag(value) {
        this._uzTag = value
    },
}

/**
 * 1. 获取分类列表
 * 使用苹果CMS V10 默认ID，如无法显示请手动修正 type_id
 */
async function getClassList(args) {
    var backData = new RepVideoClassList()
    backData.data = [
        { type_id: '1', type_name: '电影', hasSubclass: false },
        { type_id: '2', type_name: '连续剧', hasSubclass: false },
        { type_id: '3', type_name: '综艺', hasSubclass: false },
        { type_id: '4', type_name: '动漫', hasSubclass: false }
    ]
    return JSON.stringify(backData)
}

async function getSubclassList(args) {
    return JSON.stringify(new RepVideoSubclassList())
}

async function getSubclassVideoList(args) {
    return JSON.stringify(new RepVideoList())
}

/**
 * 2. 获取分类视频列表
 */
async function getVideoList(args) {
    var backData = new RepVideoList()
    // 构造URL: /index.php/vod/show/id/1/page/1.html
    let url = UZUtils.removeTrailingSlash(appConfig.webSite) +
              `/index.php/vod/show/id/${args.url}/page/${args.page}.html`

    try {
        const pro = await req(url)
        backData.error = pro.error
        if (pro.data) {
            const $ = cheerio.load(pro.data)
            let videos = []

            // 兼容多种模板选择器 (MxPro, 默认模板, 海螺等)
            let items = $('.module-item')
            if (items.length === 0) items = $('.vodlist_item')
            if (items.length === 0) items = $('.stui-vodlist__thumb')

            items.each((_, e) => {
                let videoDet = new VideoDetail()

                // 获取链接和标题
                let aTag = $(e).find('.module-item-pic a').first()
                if (aTag.length === 0) aTag = $(e).find('a').first()

                let imgTag = $(e).find('img').first()

                videoDet.vod_id = aTag.attr('href')
                videoDet.vod_name = aTag.attr('title') || imgTag.attr('alt')

                // 获取图片 (处理懒加载)
                videoDet.vod_pic = imgTag.attr('data-src') || imgTag.attr('data-original') || imgTag.attr('src')
                videoDet.vod_pic = combineUrl(videoDet.vod_pic)

                // 获取状态 (右上角文字)
                let remarks = $(e).find('.module-item-text').text() ||
                              $(e).find('.pic_text').text() ||
                              $(e).find('.pic-text').text()
                videoDet.vod_remarks = remarks ? remarks.trim() : ''

                videos.push(videoDet)
            })
            backData.data = videos
        }
    } catch (error) {
        backData.error = '列表解析错误: ' + error
    }
    return JSON.stringify(backData)
}

/**
 * 3. 获取视频详情 (解析播放列表)
 */
async function getVideoDetail(args) {
    var backData = new RepVideoDetail()
    try {
        let webUrl = combineUrl(args.url)
        let pro = await req(webUrl)

        if (pro.data) {
            const $ = cheerio.load(pro.data)
            let vodDetail = new VideoDetail()
            vodDetail.vod_id = args.url

            // 3.1 基础信息
            let titleEl = $('.page-title')
            vodDetail.vod_name = titleEl.length > 0 ? titleEl.text().trim() : $('h1').text().trim()

            let img = $('.detail_pic img, .module-item-pic img').first()
            vodDetail.vod_pic = combineUrl(img.attr('data-src') || img.attr('src'))

            // 3.2 简介
            vodDetail.vod_content = $('.content_desc span, .video-info-content, .content_detail').text().trim()

            // 3.3 解析播放线路
            let playFroms = []
            let playUrls = []

            // 查找线路 Tab
            let fromItems = $('.module-tab-item, .play_source_tab a, .nav-tabs li a')
            fromItems.each((i, e) => {
                let name = $(e).find('span').text() || $(e).text()
                // 清理多余字符
                name = name.replace(/播放|来源/g, '').trim()
                if (name) playFroms.push(name)
            })

            // 查找线路对应的剧集列表
            let listItems = $('.module-play-list-content, .playlist_notfull, .stui-content__playlist')

            listItems.each((i, e) => {
                let urls = []
                $(e).find('a').each((j, a) => {
                    let epName = $(a).text().trim()
                    let epUrl = $(a).attr('href')
                    if (epUrl) {
                        urls.push(`${epName}$${epUrl}`)
                    }
                })
                playUrls.push(urls.join('#'))
            })

            // 组合数据
            vodDetail.vod_play_from = playFroms.join('$$$')
            vodDetail.vod_play_url = playUrls.join('$$$')

            backData.data = vodDetail
        }
    } catch (error) {
        backData.error = '详情解析错误: ' + error
    }
    return JSON.stringify(backData)
}

/**
 * 4. 获取真实播放地址 (核心改进版)
 */
async function getVideoPlayUrl(args) {
    var backData = new RepVideoPlayUrl()
    try {
        let webUrl = combineUrl(args.url)

        // 发起请求时带上 Referer，防止防盗链拦截
        let pro = await req(webUrl, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Referer': appConfig.webSite
            }
        })

        if (pro.data) {
            const html = pro.data

            // 策略A：尝试解析 Maccms 播放器变量 player_aaaa
            let jsonMatch = html.match(/player_aaaa\s*=\s*({.*?});/)

            if (jsonMatch && jsonMatch[1]) {
                let playerConfig = JSON.parse(jsonMatch[1])
                let url = playerConfig.url
                let encrypt = playerConfig.encrypt // 0:不加密, 1:escape, 2:base64

                // 解码逻辑
                if (encrypt == 1) {
                    url = unescape(url)
                } else if (encrypt == 2) {
                    url = unescape(base64Decode(url))
                }

                // 判断结果类型
                if (url.indexOf('.m3u8') > -1 || url.indexOf('.mp4') > -1) {
                    // 直链直接播放
                    backData.data = url
                } else if (url.startsWith('http')) {
                    // 包含http的链接，通常是云解析地址，返回给APP，APP会自动嗅探
                    backData.data = url
                } else {
                    // 只有ID的情况，寻找页面内的iframe
                    backData.data = extractIframeUrl(html)
                }
            } else {
                // 策略B：没有找到变量，暴力查找 iframe
                backData.data = extractIframeUrl(html)
            }
        }
    } catch (error) {
        backData.error = '解析播放地址失败: ' + error
    }
    return JSON.stringify(backData)
}

/**
 * 5. 搜索视频
 */
async function searchVideo(args) {
    var backData = new RepVideoList()
    // 构造搜索URL
    let url = UZUtils.removeTrailingSlash(appConfig.webSite) +
              `/index.php/vod/search/page/${args.page}/wd/${args.searchWord}.html`
    try {
        let pro = await req(url)
        if (pro.data) {
            const $ = cheerio.load(pro.data)
            // 搜索结果通用选择器
            let items = $('.module-search-item, .searchlist_item, .stui-vodlist__media li')

            items.each((_, e) => {
                let video = new VideoDetail()
                // 尝试适配 MxPro 搜索结构
                let aTag = $(e).find('.video-serial')[0] || $(e).find('a[href*="vod/detail"]')[0]
                let imgTag = $(e).find('img')[0]

                if (aTag) {
                    video.vod_id = $(aTag).attr('href')
                    // 标题获取，优先 title 属性，其次 alt，其次文本
                    video.vod_name = $(aTag).attr('title') || $(imgTag).attr('alt') || $(e).find('h3 a').text().trim()
                    video.vod_pic = combineUrl($(imgTag).attr('data-src') || $(imgTag).attr('src'))
                    video.vod_remarks = $(e).find('.video-serial').text().trim() || $(e).find('.pic_text').text().trim()

                    backData.data.push(video)
                }
            })
        }
    } catch (error) {
        backData.error = error
    }
    return JSON.stringify(backData)
}

// === 辅助工具函数 ===

/**
 * URL 拼接与修复
 */
function combineUrl(url) {
    if (!url) return ''
    if (url.startsWith('http')) return url
    if (url.startsWith('//')) return 'http:' + url
    let baseUrl = UZUtils.removeTrailingSlash(appConfig.webSite)
    if (!url.startsWith('/')) url = '/' + url
    return baseUrl + url
}

/**
 * 提取 iframe 地址 (保底策略)
 */
function extractIframeUrl(html) {
    const $ = cheerio.load(html)
    // 优先找 player_iframe 容器
    let iframeSrc = $('#player_iframe iframe').attr('src')
    // 其次找任意包含 http 的 iframe
    if (!iframeSrc) {
        iframeSrc = $('iframe[src*="http"]').attr('src')
    }
    // 过滤掉广告iframe
    if (iframeSrc && iframeSrc.indexOf('ad') === -1) {
        return iframeSrc
    }
    return ''
}

/**
 * Base64 解码 (兼容非浏览器环境)
 */
function base64Decode(str) {
    try {
        if (typeof atob !== 'undefined') return atob(str);
        // Polyfill for UZ environment if atob missing
        var c1, c2, c3, c4;
        var i, len, out;
        var base64DecodeChars = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1, -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1];
        len = str.length;
        i = 0;
        out = "";
        while (i < len) {
            do { c1 = base64DecodeChars[str.charCodeAt(i++) & 0xff]; } while (i < len && c1 == -1);
            if (c1 == -1) break;
            do { c2 = base64DecodeChars[str.charCodeAt(i++) & 0xff]; } while (i < len && c2 == -1);
            if (c2 == -1) break;
            out += String.fromCharCode((c1 << 2) | ((c2 & 0x30) >> 4));
            do { c3 = str.charCodeAt(i++) & 0xff; if (c3 == 61) return out; c3 = base64DecodeChars[c3]; } while (i < len && c3 == -1);
            if (c3 == -1) break;
            out += String.fromCharCode(((c2 & 0XF) << 4) | ((c3 & 0x3C) >> 2));
            do { c4 = str.charCodeAt(i++) & 0xff; if (c4 == 61) return out; c4 = base64DecodeChars[c4]; } while (i < len && c4 == -1);
            if (c4 == -1) break;
            out += String.fromCharCode(((c3 & 0x03) << 6) | c4);
        }
        return out;
    } catch (e) {
        return str;
    }
}
