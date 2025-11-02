// ignore
<<<<<<< HEAD
import { createCheerio } from 'https://gitee.com/lu228826/box/raw/master/uz/js/cheerio.js'
import { createCryptoJS } from 'https://gitee.com/lu228826/box/raw/master/uz/js/CryptoJS.min.js'
import { loadJSEncrypt } from 'https://gitee.com/lu228826/box/raw/master/uz/js/JSEncrypt.min.js'
import { JSONbig } from 'https://gitee.com/lu228826/box/raw/master/uz/js/JSONbig.js'
import { createBuffer } from 'https://gitee.com/lu228826/box/raw/master/uz/js/buffer.js'
import { node_html_parser } from 'https://gitee.com/lu228826/box/raw/master/uz/js/node-html-parser.js'
=======
import { createCheerio } from './cheerio.js'
import { createCryptoJS } from './CryptoJS.min.js'
import { loadJSEncrypt } from './JSEncrypt.min.js'
import { JSONbig } from './JSONbig.js'
import { createBuffer } from './buffer.js'
import { node_html_parser } from './node-html-parser.js'
>>>>>>> 26ca3a8e4a910e6e761ad804f7eea5dcb750a3d1
// ignore

// 推荐优先使用 cheerio, parse 后期可能会移除
const parse = node_html_parser.parse

const cheerio = createCheerio()
const Crypto = createCryptoJS()
const Encrypt = loadJSEncrypt()
const BufferLib = createBuffer()
const Buffer = BufferLib.Buffer
// const SlowBuffer = BufferLib.SlowBuffer
// const Blob = BufferLib.Blob
// const File = BufferLib.File
// const atob = BufferLib.atob
// const btoa = BufferLib.btoa
// const INSPECT_MAX_BYTES = BufferLib.INSPECT_MAX_BYTES
// const kMaxLength = BufferLib.kMaxLength
// const kStringMaxLength = BufferLib.kStringMaxLength
// const constants = BufferLib.constants

// ignore
export { cheerio, Crypto, Encrypt, JSONbig, Buffer }
// ignore
