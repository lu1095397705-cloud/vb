//@name:[盘] 小米
//@version:4
//@webSite:http://xiaomi666.fun
//@remark:
//@order: A07
// 上面是插件的元数据配置，定义了名称、版本、目标站点和排序优先级。

// 全局配置对象
const appConfig = {
    // 目标网站的基础地址
    _webSite: 'http://xiaomi666.fun',

    /**
     * 网站主页，uz 调用每个函数前都会进行赋值操作
     * 如果不想被改变 请自定义一个变量
     */
    get webSite() {
        return this._webSite
    },
    set webSite(value) {
        this._webSite = value
    },

    _uzTag: '',
    /**
     * 扩展标识，初次加载时，uz 会自动赋值，请勿修改
     * 用于读取环境变量，区分不同配置
     */
    get uzTag() {
        return this._uzTag
    },
    set uzTag(value) {
        this._uzTag = value
    },
}

/**
 * 异步获取分类列表的方法。
 * 这是 APP 首页顶部的导航栏分类。
 * @param {UZArgs} args
 * @returns {Promise<RepVideoClassList>}
 */
async function getClassList(args) {
    var backData = new RepVideoClassList()
    // 这里采用硬编码（Hardcoded）方式，直接写死了分类。
    // type_id 对应网站 URL 中的分类参数，例如 /id/1.html
    backData.data = [
        {
            type_id: '1',
            type_name: '电影',
            hasSubclass: false, // 表示该分类下没有二级筛选（如按年份、地区）
        },
        {
            type_id: '2',
            type_name: '电视剧',
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

// 获取二级分类列表（筛选器），当前未实现，直接返回空
async function getSubclassList(args) {
    let backData = new RepVideoSubclassList()
    return JSON.stringify(backData)
}

// 获取二级分类对应的视频列表，当前未实现，直接返回空
async function getSubclassVideoList(args) {
    var backData = new RepVideoList()
    return JSON.stringify(backData)
}

/**
 * 获取分类视频列表
 * 当用户点击某个分类时调用此函数
 * @param {UZArgs} args
 * @returns {Promise<RepVideoList>}
 */
async function getVideoList(args) {
    var backData = new RepVideoList()
    // 构造请求 URL。args.url 是分类ID，args.page 是页码
    // 结果类似: http://www.miqk.cc/index.php/vod/show/id/1/page/1.html
    let url =
        UZUtils.removeTrailingSlash(appConfig.webSite) +
        `/index.php/vod/show/id/${args.url}/page/${args.page}.html`
    try {
        // req 是环境内置的网络请求函数
        const pro = await req(url)
        backData.error = pro.error
        let videos = []
        // 如果请求成功并返回了数据
        if (pro.data) {
            // 使用 cheerio 解析 HTML
            const $ = cheerio.load(pro.data)
            // 查找所有视频列表项，CSS选择器定位到 #main 下的 .module-item
            let vodItems = $('#main .module-item')

            // 遍历每一个找到的视频元素
            vodItems.each((_, e) => {
                let videoDet = new VideoDetail()
                // 提取详情页链接，作为 vod_id
                videoDet.vod_id = $(e).find('.module-item-pic a').attr('href')
                // 提取图片 alt 属性作为视频名称
                videoDet.vod_name = $(e)
                    .find('.module-item-pic img')
                    .attr('alt')
                // 提取图片地址 (通常使用 data-src 实现懒加载)
                videoDet.vod_pic = $(e)
                    .find('.module-item-pic img')
                    .attr('data-src')
                // 提取右上角的备注（如：更新至8集、4K等）
                videoDet.vod_remarks = $(e).find('.module-item-text').text()
                // 提取年份
                videoDet.vod_year = $(e)
                    .find('.module-item-caption span')
                    .first()
                    .text()
                videos.push(videoDet)
            })
        }
        backData.data = videos
    } catch (error) {
        // 异常处理
    }
    return JSON.stringify(backData)
}

/**
 * 获取视频详情
 * 进入具体视频页面后调用，用于提取简介、导演、网盘链接等
 * @param {UZArgs} args
 * @returns {Promise<RepVideoDetail>}
 */
async function getVideoDetail(args) {
    var backData = new RepVideoDetail()
    try {
        // 构造详情页完整 URL
        let webUrl = UZUtils.removeTrailingSlash(appConfig.webSite) + args.url
        let pro = await req(webUrl)

        backData.error = pro.error
        let proData = pro.data
        if (proData) {
            const $ = cheerio.load(proData)
            let vodDetail = new VideoDetail()
            vodDetail.vod_id = args.url
            // 提取标题
            vodDetail.vod_name = $('.page-title')[0].children[0].data
            // 提取详情页的大图
            vodDetail.vod_pic = $($('.mobile-play')).find(
                '.lazyload'
            )[0].attribs['data-src']

            // 获取详情信息块（导演、主演、剧情等标题）
            let video_items = $('.video-info-itemtitle')

            // 遍历这些信息块，解析具体内容
            for (const item of video_items) {
                let key = $(item).text() // 获取标题，如 "剧情："

                // 获取对应的内容文本
                let vItems = $(item).next().find('a')
                let value = vItems
                    .map((i, el) => {
                        let text = $(el).text().trim()
                        return text ? text : null
                    })
                    .get()
                    .filter(Boolean)
                    .join(', ')

                // 根据标题关键字判断内容类型并赋值
                if (key.includes('剧情')) {
                    // 剧情简介通常在 <p> 标签里，特殊处理
                    vodDetail.vod_content = $(item)
                        .next()
                        .find('p')
                        .text()
                        .trim()
                } else if (key.includes('导演')) {
                    vodDetail.vod_director = value.trim()
                } else if (key.includes('主演')) {
                    vodDetail.vod_actor = value.trim()
                }
            }

            // === 关键部分：提取网盘链接 ===
            const panUrls = []
            // 定位到包含分享链接的行
            let items = $('.module-row-info')
            for (const item of items) {
                // 提取 p 标签内的文本，通常是网盘链接
                let shareUrl = $(item).find('p')[0].children[0].data
                panUrls.push(shareUrl)
            }
            // 将提取到的链接赋值给 vodDetail.panUrls
            // APP 会识别这个字段来展示“转存”或“打开”按钮
            vodDetail.panUrls = panUrls
            console.log(panUrls)

            backData.data = vodDetail
        }
    } catch (error) {
        backData.error = '获取视频详情失败' + error
    }

    return JSON.stringify(backData)
}

/**
 * 获取视频的播放地址
 * @param {UZArgs} args
 * @returns {Promise<RepVideoPlayUrl>}
 */
async function getVideoPlayUrl(args) {
    var backData = new RepVideoPlayUrl()
    // 这是一个“网盘”类插件，资源通过 panUrls 返回。
    // 不需要解析具体的 m3u8/mp4 播放地址，所以这里返回空即可。
    return JSON.stringify(backData)
}

/**
 * 搜索视频
 * @param {UZArgs} args
 * @returns {Promise<RepVideoList>}
 */
async function searchVideo(args) {
    var backData = new RepVideoList()
    try {
        // 构造搜索 URL，wd=关键词
        let searchUrl = `${UZUtils.removeTrailingSlash(
            appConfig.webSite
        )}/index.php/vod/search/page/${args.page}/wd/${args.searchWord}.html`

        let repData = await req(searchUrl)
        const $ = cheerio.load(repData.data)
        // 定位搜索结果列表项
        let items = $('.module-search-item')

        // 遍历搜索结果
        for (const item of items) {
            let video = new VideoDetail()
            // 提取 ID (href)
            video.vod_id = $(item).find('.video-serial')[0].attribs.href
            // 提取 标题 (title)
            video.vod_name = $(item).find('.video-serial')[0].attribs.title
            // 提取 图片
            video.vod_pic = $(item).find('.module-item-pic > img')[0].attribs[
                'data-src'
            ]
            // 提取 备注/状态
            video.vod_remarks = $($(item).find('.video-serial')[0]).text()
            backData.data.push(video)
        }
    } catch (error) {
        backData.error = error
    }
    return JSON.stringify(backData)
}

// 辅助函数：处理 URL 拼接，防止多余的斜杠或缺少域名
function combineUrl(url) {
    if (url === undefined) {
        return ''
    }
    if (url.indexOf(appConfig.webSite) !== -1) {
        return url
    }
    if (url.startsWith('/')) {
        return appConfig.webSite + url
    }
    return appConfig.webSite + '/' + url
}
