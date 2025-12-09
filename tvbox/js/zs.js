// 迷情看 (miqk.cc) - 网盘/在线混合适配版
// 2023-12

const siteUrl = "http://www.miqk.cc";
const siteName = "迷情看(网盘版)";
const userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36";

const headers = {
    "User-Agent": userAgent,
    "Referer": siteUrl
};

async function request(url) {
    try {
        const res = await req(url, { headers: headers });
        return res.content;
    } catch (e) {
        return "";
    }
}

async function init(cfg) {
    console.log("Init: " + siteName);
}

// 首页分类 (根据实际情况调整)
async function home(filter) {
    const classes = [
        { type_id: "1", type_name: "电影" },
        { type_id: "2", type_name: "连续剧" },
        { type_id: "3", type_name: "综艺" },
        { type_id: "4", type_name: "动漫" }
    ];
    return JSON.stringify({
        class: classes,
        filters: {}
    });
}

async function homeVod() {
    return JSON.stringify({ list: [] });
}

// 分类列表
async function category(tid, pg, filter, extend) {
    const page = pg || 1;
    if (page == 0) page = 1;
    const link = `${siteUrl}/vodtype/${tid}-${page}.html`;
    const html = await request(link);
    let videos = [];

    const pattern = /class="stui-vodlist__thumb[^"]*"[\s\S]*?href="([^"]+)"[\s\S]*?title="([^"]+)"[\s\S]*?data-original="([^"]+)"[\s\S]*?class="pic-text[^"]*">([^<]+)<\/span>/g;
    let match;
    while ((match = pattern.exec(html)) !== null) {
        videos.push({
            vod_id: match[1],
            vod_name: match[2],
            vod_pic: match[3],
            vod_remarks: match[4]
        });
    }

    return JSON.stringify({
        page: parseInt(page),
        pagecount: videos.length < 20 ? page : parseInt(page) + 1,
        limit: 20,
        total: 999,
        list: videos
    });
}

// === 重点修改：详情页解析 ===
async function detail(id) {
    const link = siteUrl + id;
    const html = await request(link);

    let vod = {
        vod_id: id,
        vod_name: "",
        vod_pic: "",
        type_name: "",
        vod_content: ""
    };

    // 1. 提取基本信息
    const nameMatch = html.match(/class="title">([^<]+)<\/h1>/);
    if (nameMatch) vod.vod_name = nameMatch[1];
    const picMatch = html.match(/class="stui-content__thumb[^"]*"[^>]*data-original="([^"]+)"/);
    if (picMatch) vod.vod_pic = picMatch[1];
    const contentMatch = html.match(/name="description" content="([^"]+)"/);
    if(contentMatch) vod.vod_content = contentMatch[1];

    // 2. 准备播放列表
    let playFrom = [];
    let playUrl = [];

    // --- A. 扫描网盘链接 (核心改进) ---
    // 很多网站会把网盘链接写在简介里，或者专门的下载区
    // 正则匹配夸克和阿里
    const quarkRegex = /(https?:\/\/pan\.quark\.cn\/s\/[a-zA-Z0-9]+)/g;
    const aliRegex = /(https?:\/\/(www\.)?aliyundrive\.com\/s\/[a-zA-Z0-9]+)/g;

    let quarkSet = new Set();
    let aliSet = new Set();

    let qMatch;
    while ((qMatch = quarkRegex.exec(html)) !== null) {
        quarkSet.add(qMatch[1]);
    }
    let aMatch;
    while ((aMatch = aliRegex.exec(html)) !== null) {
        aliSet.add(aMatch[1]);
    }

    // 如果找到了夸克链接
    if (quarkSet.size > 0) {
        playFrom.push("夸克网盘");
        let urls = [];
        quarkSet.forEach(url => {
            urls.push("点击播放$" + url);
        });
        playUrl.push(urls.join("#"));
    }

    // 如果找到了阿里链接
    if (aliSet.size > 0) {
        playFrom.push("阿里云盘");
        let urls = [];
        aliSet.forEach(url => {
            urls.push("点击播放$" + url);
        });
        playUrl.push(urls.join("#"));
    }

    // --- B. 扫描原有的在线播放列表 (保留以防万一) ---
    const playListPattern = /<ul class="stui-content__playlist[\s\S]*?<\/ul>/g;
    let playListMatches = html.match(playListPattern);
    if (playListMatches) {
        for (let i = 0; i < playListMatches.length; i++) {
            let oneList = [];
            const linkPattern = /href="([^"]+)"[^>]*>([^<]+)<\/a>/g;
            let linkMatch;
            while ((linkMatch = linkPattern.exec(playListMatches[i])) !== null) {
                oneList.push(linkMatch[2] + "$" + linkMatch[1]);
            }
            if (oneList.length > 0) {
                playFrom.push("在线线路" + (i + 1));
                playUrl.push(oneList.join("#"));
            }
        }
    }

    vod.vod_play_from = playFrom.join("$$$");
    vod.vod_play_url = playUrl.join("$$$");

    return JSON.stringify({
        list: [vod]
    });
}

// === 重点修改：播放解析 ===
async function play(flag, id, flags) {
    // 1. 如果是网盘链接，直接返回，不嗅探
    if (id.indexOf("pan.quark.cn") > -1 || id.indexOf("aliyundrive.com") > -1) {
        return JSON.stringify({
            parse: 0, // 0 = 直接播放(交给Jar处理)
            url: id,
            header: headers
        });
    }

    // 2. 如果是普通网页链接，开启嗅探
    return JSON.stringify({
        parse: 1, // 1 = 嗅探
        url: siteUrl + id,
        header: headers
    });
}

async function search(wd, quick) {
    const link = `${siteUrl}/vodsearch/-------------.html?wd=${encodeURIComponent(wd)}`;
    const html = await request(link);
    let videos = [];
    const pattern = /class="stui-vodlist__thumb[^"]*"[\s\S]*?href="([^"]+)"[\s\S]*?title="([^"]+)"[\s\S]*?data-original="([^"]+)"[\s\S]*?class="pic-text[^"]*">([^<]+)<\/span>/g;
    let match;
    while ((match = pattern.exec(html)) !== null) {
        videos.push({
            vod_id: match[1],
            vod_name: match[2],
            vod_pic: match[3],
            vod_remarks: match[4]
        });
    }
    return JSON.stringify({ list: videos });
}

export default {
    init: init,
    home: home,
    homeVod: homeVod,
    category: category,
    detail: detail,
    play: play,
    search: search
};
