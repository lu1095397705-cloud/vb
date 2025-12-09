//@name:小米影视
//@version:1.0.0
//@webSite:http://xiaomi666.fun
//@remark:通用Maccms V10适配，支持在线播放
//@order: A02
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
 * 获取分类列表
 * 采用Maccms默认分类ID，如果站点进行了改动，可能需要调整 type_id
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
 * 获取视频列表
 * 兼容 MxPro (.module-item) 和 通用模板 (.vodlist_item, .stui-vodlist__thumb)
 */
async function getVideoList(args) {
    var backData = new RepVideoList()
    // 构造通用列表页 URL
    let url = UZUtils.removeTrailingSlash(appConfig.webSite) +
              `/index.php/vod/show/id/${args.url}/page/${args.page}.html`

    try {
        const pro = await req(url)
        backData.error = pro.error
        if (pro.data) {
            const $ = cheerio.load(pro.data)
            let videos = []

            // 尝试多种选择器
            let items = $('.module-item')
            if (items.length === 0) items = $('.vodlist_item')
            if (items.length === 0) items = $('.stui-vodlist__thumb') // 某些传统模板

            items.each((_, e) => {
                let videoDet = new VideoDetail()
                let aTag = $(e).find('a').first()
                let imgTag = $(e).find('img').first()

                // 处理 MxPro 的特殊结构
                if ($(e).find('.module-item-pic a').length > 0) {
                    aTag = $(e).find('.module-item-pic a')
                }

                videoDet.vod_id = aTag.attr('href')
                videoDet.vod_name = aTag.attr('title') || imgTag.attr('alt')

                // 处理懒加载图片
                videoDet.vod_pic = imgTag.attr('data-src') || imgTag.attr('data-original') || imgTag.attr('src')
                if (videoDet.vod_pic && !videoDet.vod_pic.startsWith('http')) {
                    videoDet.vod_pic = combineUrl(videoDet.vod_pic)
                }

                // 处理更新状态 (右标)
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
 * 获取视频详情
 * 解析播放列表
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

            // 1. 基础信息
            vodDetail.vod_name = $('h1').text().trim()
            let img = $('.detail_pic img, .module-item-pic img').first()
            vodDetail.vod_pic = img.attr('data-src') || img.attr('src')
            if (vodDetail.vod_pic && !vodDetail.vod_pic.startsWith('http')) {
                vodDetail.vod_pic = combineUrl(vodDetail.vod_pic)
            }

            // 简介
            vodDetail.vod_content = $('.content_desc, .video-info-content').text().trim()

            // 导演主演 (尝试抓取，如果不匹配则留空)
            let infoText = $('.video-info-main, .content_detail').text()
            if(infoText) {
                // 简单的正则匹配提取（可选）
            }

            // 2. 播放列表解析
            let playFroms = []
            let playUrls = []

            // 定位播放源 Tab
            let fromItems = $('.play_source_tab a, .module-tab-item, .nav-tabs li a')
            fromItems.each((i, e) => {
                let name = $(e).text().replace(/播放|来源/g, '').trim()
                if (name) playFroms.push(name)
            })

            // 定位播放列表容器
            let listItems = $('.playlist_notfull, .module-play-list-content, .stui-content__playlist')

            listItems.each((i, e) => {
                let urls = []
                $(e).find('a').each((j, a) => {
                    let name = $(a).text().trim()
                    let link = $(a).attr('href')
                    if (link) {
                        urls.push(`${name}$${link}`)
                    }
                })
                playUrls.push(urls.join('#'))
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
 * 获取真实播放地址
 * 提取 player_aaaa 变量
 */
async function getVideoPlayUrl(args) {
    var backData = new RepVideoPlayUrl()
    try {
        let webUrl = combineUrl(args.url)
        let pro = await req(webUrl)

        if (pro.data) {
            const $ = cheerio.load(pro.data)

            // 核心逻辑：提取 Maccms 播放器配置 json
            let scriptContent = $('script:contains("player_aaaa")').html()
            if (scriptContent) {
                let jsonMatch = scriptContent.match(/player_aaaa\s*=\s*({.*?});/)
                if (jsonMatch && jsonMatch[1]) {
                    let playerConfig = JSON.parse(jsonMatch[1])
                    // playerConfig.url 通常是加密的或者直链
                    // UZ环境通常会自动处理常见的m3u8，如果需要解密需额外逻辑
                    // 暂时直接返回 url，大部分站点现已不怎么深度加密
                    backData.data = playerConfig.url
                }
            }

            // 如果没找到脚本，尝试找 iframe
            if (!backData.data) {
                let iframe = $('iframe[src*="m3u8"], iframe[src*="mp4"]').first()
                if (iframe.length > 0) {
                    backData.data = iframe.attr('src')
                }
            }
        }
    } catch (error) {
        backData.error = '解析播放地址失败: ' + error
    }
    return JSON.stringify(backData)
}

/**
 * 搜索视频
 */
async function searchVideo(args) {
    var backData = new RepVideoList()
    // 通用搜索 URL
    let url = UZUtils.removeTrailingSlash(appConfig.webSite) +
              `/index.php/vod/search/page/${args.page}/wd/${args.searchWord}.html`
    try {
        let pro = await req(url)
        if (pro.data) {
            const $ = cheerio.load(pro.data)
            // 搜索结果列表选择器
            let items = $('.module-search-item, .searchlist_item, .stui-vodlist__media')

            items.each((_, e) => {
                let video = new VideoDetail()
                // 寻找详情链接
                let aTag = $(e).find('a[href*="vod/detail"]').first()
                // 寻找图片
                let imgTag = $(e).find('img').first()

                if (aTag.length > 0) {
                    video.vod_id = aTag.attr('href')
                    video.vod_name = aTag.attr('title') || imgTag.attr('alt') || $(e).find('h3, h4').text().trim()
                    video.vod_pic = imgTag.attr('data-src') || imgTag.attr('src')
                    if (video.vod_pic && !video.vod_pic.startsWith('http')) {
                        video.vod_pic = combineUrl(video.vod_pic)
                    }

                    // 状态
                    let remarks = $(e).find('.video-serial, .pic_text, .pic-text').text()
                    video.vod_remarks = remarks ? remarks.trim() : ''

                    backData.data.push(video)
                }
            })
        }
    } catch (error) {
        backData.error = error
    }
    return JSON.stringify(backData)
}

// 辅助函数：处理 URL 拼接
function combineUrl(url) {
    if (!url) return ''
    if (url.startsWith('http')) return url
    // 移除末尾斜杠 + 移除开头斜杠 = 避免双斜杠
    let baseUrl = UZUtils.removeTrailingSlash(appConfig.webSite)
    if (!url.startsWith('/')) url = '/' + url
    return baseUrl + url
}
