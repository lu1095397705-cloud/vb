import json

# TVBox配置数据
config = {
    "sites": [
        {
            "key": "miqk",
            "name": "米奇妙资源站",
            "type": 1,
            "api": "https://www.miqk.cc/api.php/provide/vod/",
            "searchable": 1,
            "quickSearch": 1,
            "filterable": 1
        }
    ],
    "parses": [
        {"name": "解析聚合", "type": 3, "url": "Demo"},
        {"name": "Web解析聚合", "type": 3, "url": "Web"},
        {"name": "线路1", "type": 1, "url": "https://jx.jsonplayer.com/player/?url="},
        {"name": "线路2", "type": 1, "url": "https://jx.777jiexi.com/player/?url="}
    ],
    "ijk": [
        {"group": "软解码", "options": [
            {"category": 4, "name": "opensles", "value": "0"},
            {"category": 4, "name": "overlay-format", "value": "842225234"},
            {"category": 4, "name": "framedrop", "value": "1"},
            {"category": 4, "name": "start-on-prepared", "value": "1"},
            {"category": 1, "name": "http-detect-range-support", "value": "0"},
            {"category": 1, "name": "fflags", "value": "fastseek"},
            {"category": 2, "name": "skip_loop_filter", "value": "48"},
            {"category": 4, "name": "reconnect", "value": "1"},
            {"category": 4, "name": "enable-accurate-seek", "value": "0"},
            {"category": 4, "name": "mediacodec", "value": "0"},
            {"category": 4, "name": "mediacodec-auto-rotate", "value": "0"},
            {"category": 4, "name": "mediacodec-handle-resolution-change", "value": "0"},
            {"category": 4, "name": "mediacodec-hevc", "value": "0"}
        ]},
        {"group": "硬解码", "options": [
            {"category": 4, "name": "opensles", "value": "0"},
            {"category": 4, "name": "overlay-format", "value": "842225234"},
            {"category": 4, "name": "framedrop", "value": "1"},
            {"category": 4, "name": "start-on-prepared", "value": "1"},
            {"category": 1, "name": "http-detect-range-support", "value": "0"},
            {"category": 1, "name": "fflags", "value": "fastseek"},
            {"category": 2, "name": "skip_loop_filter", "value": "48"},
            {"category": 4, "name": "reconnect", "value": "1"},
            {"category": 4, "name": "enable-accurate-seek", "value": "0"},
            {"category": 4, "name": "mediacodec", "value": "1"},
            {"category": 4, "name": "mediacodec-auto-rotate", "value": "1"},
            {"category": 4, "name": "mediacodec-handle-resolution-change", "value": "1"},
            {"category": 4, "name": "mediacodec-hevc", "value": "1"}
        ]}
    ],
    "ads": [
        "mimg.127.net",
        "www.127.net",
        "haitu.tv",
        "player.bilibili.com",
        "s1.hdslb.com"
    ]
}

# 保存配置文件
with open("tvbox_config.json", "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print("TVBox配置文件已生成: tvbox_config.json")
print("使用方法：在TVBox中添加此文件作为配置源")