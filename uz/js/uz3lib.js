// ignore
import { createCheerio } from './js/cheerio.js'
import { createCryptoJS } from './js/CryptoJS.min.js'
import { loadJSEncrypt } from './js/JSEncrypt.min.js'
import { JSONbig } from './js/JSONbig.js'
import { createBuffer } from './js/buffer.js'
import { node_html_parser } from './js/node-html-parser.js'
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
