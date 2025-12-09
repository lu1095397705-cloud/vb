//@name:小米影视
//@version:1.0.8
//@webSite:http://xiaomi666.fun
//@remark:修复播放列表获取失败问题，增强兼容性
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

            // 兼容多种模板列表选择器
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

                    let remarks = $(e).find('.module-item-text').text() ||
                                  $(e).find('.pic_text').text() ||
                                  $(e).find('.pic-text').text()
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
 * 3. 获取视频详情 (深度修复版)
 */
async function getVideoDetail(args) {
    var backData = new RepVideoDetail()
    try {
        let webUrl = combineUrl(args.url)

        // 关键修复：添加 Headers，防止服务器返回不完整的 HTML
        let pro = await req(webUrl, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
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
            let imgSrc = img.attr('data-src') || img.attr('src')
            vodDetail.vod_pic = combineUrl(imgSrc)

            let desc = $('.module-info-introduction-content, .video-info-content, .content_desc').text().trim()
            vodDetail.vod_content = desc

            // --- 播放列表解析 (增强版) ---

            let playFroms = []
            let playUrls = []

            // 1. 查找所有可能的播放列表容器
            // MxPro: .module-play-list -> .module-play-list-content
            // 通用: .stui-content__playlist, .playlist_notfull
            let playlistNodes = $('.module-play-list-content')
            if (playlistNodes.length === 0) playlistNodes = $('.module-play-list') // 退一步找外层
            if (playlistNodes.length === 0) playlistNodes = $('.stui-content__playlist')
            if (playlistNodes.length === 0) playlistNodes = $('.playlist_notfull')

            // 2. 查找线路名称 Tab
            // MxPro: .module-tab-item
            // 通用: .play_source_tab a
            let tabNodes = $('.module-tab-item')
            if (tabNodes.length === 0) tabNodes = $('.play_source_tab a, .nav-tabs li a')

            // 3. 遍历提取
            playlistNodes.each((i, e) => {
                let urls = []
                let aLinks = $(e).find('a') // 查找容器内所有链接

                aLinks.each((j, a) => {
                    let epName = $(a).find('span').text() || $(a).text()
                    epName = epName.trim()
                    let epUrl = $(a).attr('href')
                    // 排除掉非播放链接（如javascript:;）
                    if (epUrl && (epUrl.startsWith('http') || epUrl.startsWith('/'))) {
                        urls.push(`${epName}$${epUrl}`)
                    }
                })

                // 只有当该列表里确实有链接时才添加
                if (urls.length > 0) {
                    // 尝试匹配线路名称
                    let fromName = `线路${i + 1}`
                    if (i < tabNodes.length) {
                        let rawName = $(tabNodes[i]).find('span').text() || $(tabNodes[i]).text()
                        rawName = rawName.replace(/播放|来源/g, '').trim()
                        if (rawName) fromName = rawName
                    }

                    playFroms.push(fromName)
                    playUrls.push(urls.join('#'))
                }
            })

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
 * 4. 获取真实播放地址 (支持网盘 & 嗅探)
 */
async function getVideoPlayUrl(args) {
    var backData = new RepVideoPlayUrl()
    try {
        let webUrl = combineUrl(args.url)

        // 必须带 Referer
        let pro = await req(webUrl, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Referer': appConfig.webSite
            }
        })

        if (pro.data) {
            const html = pro.data

            // 提取 Maccms 播放器变量
            let jsonMatch = html.match(/player_aaaa\s*=\s*({.*?});/)

            if (jsonMatch && jsonMatch[1]) {
                let playerConfig = JSON.parse(jsonMatch[1])
                let url = playerConfig.url
                let encrypt = playerConfig.encrypt

                if (encrypt == 1) {
                    url = unescape(url)
                } else if (encrypt == 2) {
                    url = unescape(base64Decode(url))
                }

                // 策略：只要是 URL 就返回，交给 APP 处理 (支持直链、网盘、云解析)
                if (url.startsWith('http')) {
                    backData.data = url
                } else {
                    // ID 类型，找 iframe
                    backData.data = extractIframeUrl(html)
                }
            } else {
                // 无变量，保底找 iframe
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
