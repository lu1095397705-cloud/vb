//@name:小米影视
//@version:1.1.0
//@webSite:http://xiaomi666.fun
//@remark:最终修复版-支持网盘/下载列表/全线路抓取
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
    let url = UZUtils.removeTrailingSlash(appConfig.webSite) +
              `/index.php/vod/show/id/${args.url}/page/${args.page}.html`

    try {
        const pro = await req(url)
        backData.error = pro.error
        if (pro.data) {
            const $ = cheerio.load(pro.data)
            let videos = []
            // 聚合多种列表选择器
            let items = $('.module-item, .vodlist_item, .stui-vodlist__thumb, .list-item')

            items.each((_, e) => {
                let videoDet = new VideoDetail()
                let aTag = $(e).find('.module-item-pic a').first()
                if (aTag.length === 0) aTag = $(e).find('a').first()
                let imgTag = $(e).find('img').first()

                if (aTag.length > 0) {
                    videoDet.vod_id = aTag.attr('href')
                    videoDet.vod_name = aTag.attr('title') || imgTag.attr('alt') || $(e).text().trim()
                    let src = imgTag.attr('data-src') || imgTag.attr('data-original') || imgTag.attr('src')
                    videoDet.vod_pic = combineUrl(src)
                    let remarks = $(e).find('.module-item-text').text() || $(e).find('.pic-text').text()
                    videoDet.vod_remarks = remarks ? remarks.trim() : ''
                    videos.push(videoDet)
                }
            })
            backData.data = videos
        }
    } catch (error) {
        backData.error = '列表解析错误: ' + error
    }
    return JSON.stringify(backData)
}

/**
 * 3. 获取视频详情 (核心修复: 网盘/下载列表)
 */
async function getVideoDetail(args) {
    var backData = new RepVideoDetail()
    try {
        let webUrl = combineUrl(args.url)
        let pro = await req(webUrl, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Referer': appConfig.webSite
            }
        })

        if (pro.data) {
            const $ = cheerio.load(pro.data)
            let vodDetail = new VideoDetail()
            vodDetail.vod_id = args.url

            // 基础信息
            let title = $('h1.page-title').text().trim() || $('h1').text().trim()
            vodDetail.vod_name = title
            let img = $('.module-item-pic img, .detail_pic img').first()
            vodDetail.vod_pic = combineUrl(img.attr('data-src') || img.attr('src'))
            vodDetail.vod_content = $('.module-info-introduction-content, .content_desc').text().trim()

            // --- 播放列表解析逻辑 ---
            let playFroms = []
            let playUrls = []

            // 1. 寻找所有可能的 Tab (线路名)
            // 包括播放线路 (.module-tab-item) 和 下载/网盘线路 (通常没有特定 class，或在 .module-tab-items 中)
            let tabContainer = $('.module-tab-items').first()
            let tabNodes = tabContainer.find('.module-tab-item')

            // 如果没找到标准 Tab，尝试旧版选择器
            if (tabNodes.length === 0) {
                tabNodes = $('.play_source_tab a, .nav-tabs li a, .module-tab-content .module-tab-item')
            }

            // 2. 寻找所有可能的 List (内容容器)
            // 关键：同时查找 "播放列表" 和 "下载列表" (.module-down-list)
            // MxPro 模板中，下载/网盘链接往往在 .module-down-list 中
            let playlistNodes = $('.module-play-list-content, .module-play-list, .stui-content__playlist, .module-down-list')

            // 3. 遍历提取
            playlistNodes.each((i, e) => {
                let urls = []
                let aLinks = $(e).find('a')

                aLinks.each((j, a) => {
                    let epName = $(a).find('span').text() || $(a).text()
                    epName = epName.replace(/[\r\n]/g, '').trim()
                    let epUrl = $(a).attr('href')

                    // 只要 href 存在且不是纯锚点/JS
                    if (epUrl && epUrl.indexOf('javascript:') === -1 && epUrl !== '#') {
                        urls.push(`${epName}$${epUrl}`)
                    }
                })

                if (urls.length > 0) {
                    // 尝试匹配线路名
                    let fromName = `线路${i + 1}`
                    // 优先从 Tab 获取名称
                    if (i < tabNodes.length) {
                        let rawName = $(tabNodes[i]).find('span').text() || $(tabNodes[i]).text()
                        rawName = rawName.replace(/播放|来源|\[|\]/g, '').trim()
                        if(rawName) fromName = rawName
                    } else {
                        // 如果 Tab 数量少于 List 数量（常见于下载列表被单独列出）
                        // 判断容器 Class，如果是 down-list，命名为“下载/网盘”
                        if ($(e).hasClass('module-down-list')) {
                            fromName = "网盘下载"
                        }
                    }

                    playFroms.push(fromName)
                    playUrls.push(urls.join('#'))
                }
            })

            // 兜底：如果上面没找到，尝试暴力搜索页面所有带 href 的列表
            if (playUrls.length === 0) {
                 // 这种情况极少见，除非页面结构完全变了
                 backData.error = "未找到有效的播放列表"
            }

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
 * 4. 获取真实播放地址
 */
async function getVideoPlayUrl(args) {
    var backData = new RepVideoPlayUrl()
    try {
        let webUrl = combineUrl(args.url)
        let pro = await req(webUrl, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Referer': appConfig.webSite
            }
        })

        if (pro.data) {
            const html = pro.data
            let jsonMatch = html.match(/player_aaaa\s*=\s*({.*?});/)

            if (jsonMatch && jsonMatch[1]) {
                let playerConfig = JSON.parse(jsonMatch[1])
                let url = playerConfig.url
                let encrypt = playerConfig.encrypt

                if (encrypt == 1) url = unescape(url)
                else if (encrypt == 2) url = unescape(base64Decode(url))

                // 只要是链接就返回，让 App 决定如何打开 (支持 http/https 直链、网盘、m3u8)
                if (url.startsWith('http')) {
                    backData.data = url
                } else {
                    backData.data = extractIframeUrl(html)
                }
            } else {
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
    let url = UZUtils.removeTrailingSlash(appConfig.webSite) +
              `/index.php/vod/search/page/${args.page}/wd/${args.searchWord}.html`
    try {
        let pro = await req(url)
        if (pro.data) {
            const $ = cheerio.load(pro.data)
            let items = $('.module-search-item, .searchlist_item')
            items.each((_, e) => {
                let video = new VideoDetail()
                let aTag = $(e).find('.video-serial')[0] || $(e).find('a[href*="vod/detail"]')[0]
                let imgTag = $(e).find('img')[0]

                if (aTag) {
                    video.vod_id = $(aTag).attr('href')
                    video.vod_name = $(e).find('h3').text().trim() || $(aTag).attr('title')
                    video.vod_pic = combineUrl($(imgTag).attr('data-src') || $(imgTag).attr('src'))
                    video.vod_remarks = $(e).find('.video-serial').text().trim()
                    backData.data.push(video)
                }
            })
        }
    } catch (error) {
        backData.error = error
    }
    return JSON.stringify(backData)
}

// === 工具函数 ===

function combineUrl(url) {
    if (!url) return ''
    if (url.startsWith('http')) return url
    if (url.startsWith('//')) return 'http:' + url
    let baseUrl = UZUtils.removeTrailingSlash(appConfig.webSite)
    if (!url.startsWith('/')) url = '/' + url
    return baseUrl + url
}

function extractIframeUrl(html) {
    const $ = cheerio.load(html)
    let iframeSrc = $('#player_iframe iframe').attr('src')
    if (!iframeSrc) {
        $('iframe').each((i, el) => {
            let src = $(el).attr('src')
            if (src && src.startsWith('http') && src.indexOf('ad') === -1) {
                iframeSrc = src
                return false
            }
        })
    }
    return iframeSrc || ''
}

function base64Decode(str) {
    try {
        if (typeof atob !== 'undefined') return atob(str);
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
