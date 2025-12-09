//@name:香山影视
//@version:1.0.0
//@webSite:http://xsayang.fun:12512
//@remark:适配Maccms V10通用模板，支持在线播放
//@order: A01
const appConfig = {
    _webSite: 'http://xsayang.fun:12512',
    /**
     * 网站主页
     */
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
 * 获取分类列表
 * 注：这里使用了Maccms通用的分类ID，如果站点不同请自行修改
 */
async function getClassList(args) {
    var backData = new RepVideoClassList()
    backData.data = [
        {
            type_id: '1',
            type_name: '电影',
            hasSubclass: false,
        },
        {
            type_id: '2',
            type_name: '剧集',
            hasSubclass: false,
        },
        {
            type_id: '3',
            type_name: '综艺',
            hasSubclass: false,
        },
        {
            type_id: '4',
            type_name: '动漫',
            hasSubclass: false,
        }
    ]
    return JSON.stringify(backData)
}

async function getSubclassList(args) {
    let backData = new RepVideoSubclassList()
    return JSON.stringify(backData)
}

async function getSubclassVideoList(args) {
    var backData = new RepVideoList()
    return JSON.stringify(backData)
}

/**
 * 获取分类视频列表
 */
async function getVideoList(args) {
    var backData = new RepVideoList()
    // 通用Maccms列表路径构造
    let url = UZUtils.removeTrailingSlash(appConfig.webSite) +
        `/index.php/vod/show/id/${args.url}/page/${args.page}.html`
    try {
        const pro = await req(url)
        backData.error = pro.error
        let videos = []
        if (pro.data) {
            const $ = cheerio.load(pro.data)
            // 尝试匹配通用列表项 (.module-item 是 MxPro 模板常用类名)
            let vodItems = $('.module-item')
            // 如果没找到，尝试匹配传统Maccms类名
            if (vodItems.length === 0) {
                 vodItems = $('.vodlist_item')
            }

            vodItems.each((_, e) => {
                let videoDet = new VideoDetail()
                // 兼容不同的DOM结构
                let aTag = $(e).find('.module-item-pic a').length > 0 ? $(e).find('.module-item-pic a') : $(e).find('a').first()
                let imgTag = $(e).find('img').first()

                videoDet.vod_id = aTag.attr('href')
                videoDet.vod_name = aTag.attr('title') || imgTag.attr('alt')
                videoDet.vod_pic = imgTag.attr('data-src') || imgTag.attr('src')
                videoDet.vod_remarks = $(e).find('.module-item-text').text() || $(e).find('.pic_text').text()

                videos.push(videoDet)
            })
        }
        backData.data = videos
    } catch (error) {
        backData.error = "列表解析失败: " + error
    }
    return JSON.stringify(backData)
}

/**
 * 获取视频详情
 * 修改点：增加了播放线路的解析，去除了网盘解析逻辑
 */
async function getVideoDetail(args) {
    var backData = new RepVideoDetail()
    try {
        let webUrl = combineUrl(args.url)
        let pro = await req(webUrl)

        backData.error = pro.error
        let proData = pro.data
        if (proData) {
            const $ = cheerio.load(proData)
            let vodDetail = new VideoDetail()
            vodDetail.vod_id = args.url

            // 解析基础信息
            let titleEl = $('.page-title')
            vodDetail.vod_name = titleEl.length > 0 ? titleEl.text().trim() : $('h1').first().text().trim()

            let picEl = $('.mobile-play .lazyload')
            vodDetail.vod_pic = picEl.length > 0 ? picEl.attr('data-src') : $('.detail_pic img').attr('src')

            // 解析详细参数 (导演、主演、简介)
            // 尝试适配多种模板结构
            let desc = $('.video-info-content p').text().trim() || $('.content_desc').text().trim()
            vodDetail.vod_content = desc

            // 解析播放列表 (核心修改：适配在线播放)
            let playFroms = []
            let playUrls = []

            // 1. 获取线路名称
            // MxPro模板通常在 .module-tab-item 或 .play_source_tab a
            let tabs = $('.module-tab-item')
            if (tabs.length === 0) tabs = $('.play_source_tab a')

            tabs.each((i, e) => {
                let name = $(e).find('span').text() || $(e).text()
                playFroms.push(name.replace('播放', '').trim())
            })

            // 2. 获取线路对应的剧集列表
            // MxPro模板内容在 .module-play-list-content
            let lists = $('.module-play-list-content')
            if (lists.length === 0) lists = $('.playlist_notfull') // 传统模板

            lists.each((i, e) => {
                let urls = []
                $(e).find('a').each((j, a) => {
                    let epName = $(a).text().trim()
                    let epUrl = $(a).attr('href')
                    urls.push(`${epName}$${epUrl}`)
                })
                playUrls.push(urls.join('#'))
            })

            vodDetail.vod_play_from = playFroms.join('$$$')
            vodDetail.vod_play_url = playUrls.join('$$$')

            backData.data = vodDetail
        }
    } catch (error) {
        backData.error = '获取视频详情失败: ' + error
    }

    return JSON.stringify(backData)
}

/**
 * 获取视频的播放地址
 * 核心修改：实现在线播放解析
 */
async function getVideoPlayUrl(args) {
    var backData = new RepVideoPlayUrl()
    try {
        let webUrl = combineUrl(args.url)
        const pro = await req(webUrl)
        if (pro.data) {
            // Maccms V10 标准播放器数据提取
            // 查找 var player_aaaa = {...} 数据
            const $ = cheerio.load(pro.data)
            let scriptData = $('script:contains("player_aaaa")').html()

            if (scriptData) {
                // 提取 JSON 字符串
                let jsonStr = scriptData.match(/player_aaaa\s*=\s*({.*?});/)
                if (jsonStr && jsonStr[1]) {
                    let playerData = JSON.parse(jsonStr[1])
                    // 如果 URL 是加密的，通常这里是直接返回或者需要简单Base64解码
                    // 大部分Maccms直接返回url，或者url在encrypt=0时是直链
                    backData.data = playerData.url

                    // 如果是m3u8直链，直接返回；如果是iframe，UZ通常也能处理，但最好能解析出直链
                    if(backData.data.indexOf('.m3u8') === -1 && backData.data.indexOf('.mp4') === -1) {
                         // 有些站点会再次嵌套，这里暂且返回原始链接
                         // 如果遇到加密，可能需要引入 UZUtils.base64Decode
                    }
                }
            } else {
                // 尝试查找 iframe
                let iframeSrc = $('iframe').attr('src')
                if (iframeSrc) backData.data = iframeSrc
            }
        }
    } catch (error) {
        backData.error = error
    }
    return JSON.stringify(backData)
}

/**
 * 搜索视频
 */
async function searchVideo(args) {
    var backData = new RepVideoList()
    try {
        // Maccms 通用搜索路径
        let searchUrl = `${UZUtils.removeTrailingSlash(appConfig.webSite)}/index.php/vod/search/page/${args.page}/wd/${args.searchWord}.html`
        let repData = await req(searchUrl)
        const $ = cheerio.load(repData.data)

        // 尝试匹配 MxPro 搜索结果
        let items = $('.module-search-item')
        if (items.length === 0) items = $('.searchlist_item') // 备用选择器

        items.each((_, item) => {
            let video = new VideoDetail()
            // 适配 MxPro
            let aTag = $(item).find('.video-serial')[0] || $(item).find('a')[0]
            let imgTag = $(item).find('img')[0]

            if (aTag) {
                video.vod_id = aTag.attribs.href
                video.vod_name = aTag.attribs.title || $(imgTag).attr('alt')
                video.vod_pic = $(imgTag).attr('data-src') || $(imgTag).attr('src')
                video.vod_remarks = $(aTag).text().trim() || $(item).find('.pic_text').text().trim()
                backData.data.push(video)
            }
        })
    } catch (error) {
        backData.error = error
    }
    return JSON.stringify(backData)
}

function combineUrl(url) {
    if (url === undefined) {
        return ''
    }
    if (url.indexOf('http') !== -1) {
        return url
    }
    if (url.startsWith('/')) {
        return UZUtils.removeTrailingSlash(appConfig.webSite) + url
    }
    return UZUtils.removeTrailingSlash(appConfig.webSite) + '/' + url
}
