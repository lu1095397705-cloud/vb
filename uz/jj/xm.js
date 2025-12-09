//@name:小米影视
//@version:1.0.5
//@webSite:http://xiaomi666.fun
//@remark:修复详情页解析，支持网盘链接跳转
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
    // 构造URL
    let url = UZUtils.removeTrailingSlash(appConfig.webSite) +
              `/index.php/vod/show/id/${args.url}/page/${args.page}.html`

    try {
        const pro = await req(url)
        backData.error = pro.error
        if (pro.data) {
            const $ = cheerio.load(pro.data)
            let videos = []

            // 适配 MxPro 及通用模板列表项
            let items = $('.module-item, .vodlist_item, .stui-vodlist__thumb')

            items.each((_, e) => {
                let videoDet = new VideoDetail()

                // 链接与图片容器
                let aTag = $(e).find('.module-item-pic a').first()
                if (aTag.length === 0) aTag = $(e).find('a').first()
                let imgTag = $(e).find('img').first()

                videoDet.vod_id = aTag.attr('href')
                videoDet.vod_name = aTag.attr('title') || imgTag.attr('alt')

                // 图片处理
                let src = imgTag.attr('data-src') || imgTag.attr('data-original') || imgTag.attr('src')
                videoDet.vod_pic = combineUrl(src)

                // 状态/集数
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
 * 3. 获取视频详情 (修复版)
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

            // --- 详情信息抓取优化 ---

            // 标题: MxPro 通常在 h1.page-title
            let title = $('h1.page-title').text().trim() || $('h1').text().trim()
            vodDetail.vod_name = title

            // 图片: 优先找 .module-item-pic
            let img = $('.module-item-pic img').first()
            if (img.length === 0) img = $('.detail_pic img').first()
            let imgSrc = img.attr('data-src') || img.attr('src')
            vodDetail.vod_pic = combineUrl(imgSrc)

            // 简介: MxPro 通常在 .module-info-introduction-content
            let desc = $('.module-info-introduction-content').text().trim()
            if (!desc) desc = $('.video-info-content').text().trim()
            if (!desc) desc = $('meta[name="description"]').attr('content')
            vodDetail.vod_content = desc

            // 导演/主演 (可选)
            // let director = $('.module-info-item:contains("导演")').text().replace('导演：', '').trim();
            // vodDetail.vod_director = director;

            // --- 播放列表抓取优化 ---

            let playFroms = []
            let playUrls = []

            // 1. 定位 Tab (线路名称)
            // MxPro 的 Tab 通常在 .module-tab-items .module-tab-item
            // 同时也兼容旧版 .play_source_tab
            let tabContainer = $('.module-tab-items').eq(0) // 通常第一个 Tab 组是播放源
            let fromItems = tabContainer.find('.module-tab-item')

            if (fromItems.length === 0) {
                // 兼容旧模板
                fromItems = $('.play_source_tab a, .nav-tabs li a')
            }

            // 2. 定位 List (剧集列表)
            let listItems = $('.module-play-list')
            if (listItems.length === 0) {
                // 兼容旧模板
                listItems = $('.playlist_notfull, .stui-content__playlist')
            }

            // 3. 遍历提取
            // 注意：有时候页面会有“下载”或“相关推荐”的 Tab，需要确保 Tab 和 List 数量对应
            // 这里的逻辑假设 Tab 和 List 是按顺序一一对应的

            let maxCount = Math.min(fromItems.length, listItems.length)

            for (let i = 0; i < maxCount; i++) {
                // 提取线路名
                let tabName = $(fromItems[i]).find('span').text() || $(fromItems[i]).text()
                tabName = tabName.replace(/播放|来源/g, '').trim()

                // 提取该线路下的所有集数
                let urls = []
                let aLinks = $(listItems[i]).find('a')

                aLinks.each((j, a) => {
                    let epName = $(a).find('span').text() || $(a).text()
                    epName = epName.trim()
                    let epUrl = $(a).attr('href')
                    if (epUrl) {
                        urls.push(`${epName}$${epUrl}`)
                    }
                })

                if (urls.length > 0) {
                    playFroms.push(tabName)
                    playUrls.push(urls.join('#'))
                }
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
 * 4. 获取真实播放地址 (支持网盘)
 */
async function getVideoPlayUrl(args) {
    var backData = new RepVideoPlayUrl()
    try {
        let webUrl = combineUrl(args.url)

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

                // 解码
                if (encrypt == 1) {
                    url = unescape(url)
                } else if (encrypt == 2) {
                    url = unescape(base64Decode(url))
                }

                // --- 关键修改：放宽判断逻辑 ---
                // 只要是 http 开头的，不管是 m3u8, mp4 还是网盘链接(share.quark等)，都直接返回
                // UZ App 会自动处理：如果是视频流则播放，如果是网页则打开 Webview 或嗅探
                if (url.startsWith('http')) {
                    backData.data = url
                } else {
                    // 如果不是 http 开头 (例如只是 ID)，则去页面找 iframe
                    backData.data = extractIframeUrl(html)
                }
            } else {
                // 没有变量，暴力找 iframe
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
            // MxPro 搜索结果选择器
            let items = $('.module-search-item')
            if (items.length === 0) items = $('.searchlist_item') // 兼容旧版

            items.each((_, e) => {
                let video = new VideoDetail()

                // MxPro 结构: .video-serial (链接), .module-item-pic img (图)
                let aTag = $(e).find('.video-serial')[0]
                if(!aTag) aTag = $(e).find('a[href*="vod/detail"]')[0]

                let imgTag = $(e).find('img')[0]

                if (aTag) {
                    video.vod_id = $(aTag).attr('href')
                    // 标题：MxPro 在 h3 里面
                    video.vod_name = $(e).find('h3').text().trim() || $(aTag).attr('title') || $(imgTag).attr('alt')
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
    // 针对 Maccms，iframe 通常在 player_iframe 容器内，或者直接是 iframe 标签
    let iframeSrc = $('#player_iframe iframe').attr('src')
    if (!iframeSrc) {
        // 查找所有 iframe，取第一个包含 http 且不是广告的
        $('iframe').each((i, el) => {
            let src = $(el).attr('src')
            if (src && src.startsWith('http') && src.indexOf('ad') === -1) {
                iframeSrc = src
                return false // break
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
