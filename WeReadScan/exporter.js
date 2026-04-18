(function() {
    'use strict';

    const $ = (typeof jQuery !== 'undefined') ? jQuery : null;
    console.log('WeReadExporter Injected.');

    class WereadGenerateBrowser {
        constructor(book_id, chapter_id, pc, ps) {
            if (!book_id || !chapter_id || !pc || !ps) {
                console.error('Missing params for decryption:', {book_id, chapter_id, pc, ps});
                throw `（book_id, chapter_id, pc, ps） all not null.`
            }
            this.book_id = book_id;
            this.chapter_id = chapter_id;
            this.pc = pc;
            this.ps = ps;
        }

        static instance() {
            return new WereadGenerateBrowser('1', '1', '1', '1')
        }

        md5_hex(message) {
            return this.#md5(message);
        }

        #md5(str) {
            function md5cycle(x, k) {
                let a = x[0], b = x[1], c = x[2], d = x[3];
                a = ff(a, b, c, d, k[0], 7, -680876936);
                d = ff(d, a, b, c, k[1], 12, -389564586);
                c = ff(c, d, a, b, k[2], 17, 606105819);
                b = ff(b, c, d, a, k[3], 22, -1044525330);
                a = ff(a, b, c, d, k[4], 7, -176418897);
                d = ff(d, a, b, c, k[5], 12, 1200080426);
                c = ff(c, d, a, b, k[6], 17, -1473231341);
                b = ff(b, c, d, a, k[7], 22, -45705983);
                a = ff(a, b, c, d, k[8], 7, 1770035416);
                d = ff(d, a, b, c, k[9], 12, -1958414417);
                c = ff(c, d, a, b, k[10], 17, -42063);
                b = ff(b, c, d, a, k[11], 22, -1990404162);
                a = ff(a, b, c, d, k[12], 7, 1804603682);
                d = ff(d, a, b, c, k[13], 12, -40341101);
                c = ff(c, d, a, b, k[14], 17, -1502002290);
                b = ff(b, c, d, a, k[15], 22, 1236535329);
                a = gg(a, b, c, d, k[1], 5, -165796510);
                d = gg(d, a, b, c, k[6], 9, -1069501632);
                c = gg(c, d, a, b, k[11], 14, 643717713);
                b = gg(b, c, d, a, k[0], 20, -373897302);
                a = gg(a, b, c, d, k[5], 5, -701558691);
                d = gg(d, a, b, c, k[10], 9, 38016083);
                c = gg(c, d, a, b, k[15], 14, -660478335);
                b = gg(b, c, d, a, k[4], 20, -405537848);
                a = gg(a, b, c, d, k[9], 5, 568446438);
                d = gg(d, a, b, c, k[14], 9, -1019803690);
                c = gg(c, d, a, b, k[3], 14, -187363961);
                b = gg(b, c, d, a, k[8], 20, 1163531501);
                a = gg(a, b, c, d, k[13], 5, -1444681467);
                d = gg(d, a, b, c, k[2], 9, -51403784);
                c = gg(c, d, a, b, k[7], 14, 1735328473);
                b = gg(b, c, d, a, k[12], 20, -1926607734);
                a = hh(a, b, c, d, k[5], 4, -378558);
                d = hh(d, a, b, c, k[8], 11, -2022574463);
                c = hh(c, d, a, b, k[11], 16, 1839030562);
                b = hh(b, c, d, a, k[14], 23, -35309556);
                a = hh(a, b, c, d, k[1], 4, -1530992060);
                d = hh(d, a, b, c, k[4], 11, 1272893353);
                c = hh(c, d, a, b, k[7], 16, -155497632);
                b = hh(b, c, d, a, k[10], 23, -1094730640);
                a = hh(a, b, c, d, k[13], 4, 681279174);
                d = hh(d, a, b, c, k[0], 11, -358537222);
                c = hh(c, d, a, b, k[3], 16, -722521979);
                b = hh(b, c, d, a, k[6], 23, 76029189);
                a = hh(a, b, c, d, k[9], 4, -640364487);
                d = hh(d, a, b, c, k[12], 11, -421815835);
                c = hh(c, d, a, b, k[15], 16, 530742520);
                b = hh(b, c, d, a, k[2], 23, -995338651);
                a = ii(a, b, c, d, k[0], 6, -198630844);
                d = ii(d, a, b, c, k[7], 10, 1126891415);
                c = ii(c, d, a, b, k[14], 15, -1416354905);
                b = ii(b, c, d, a, k[5], 21, -57434055);
                a = ii(a, b, c, d, k[12], 6, 1700485571);
                d = ii(d, a, b, c, k[3], 10, -1894986606);
                c = ii(c, d, a, b, k[10], 15, -1051523);
                b = ii(b, c, d, a, k[1], 21, -2054922799);
                a = ii(a, b, c, d, k[8], 6, 1873313359);
                d = ii(d, a, b, c, k[15], 10, -30611744);
                c = ii(c, d, a, b, k[6], 15, -1560198380);
                b = ii(b, c, d, a, k[13], 21, 1309151649);
                a = ii(a, b, c, d, k[4], 6, -145523070);
                d = ii(d, a, b, c, k[11], 10, -1120210379);
                c = ii(c, d, a, b, k[2], 15, 718787259);
                b = ii(b, c, d, a, k[9], 21, -343485551);
                x[0] = add32(a, x[0]);
                x[1] = add32(b, x[1]);
                x[2] = add32(c, x[2]);
                x[3] = add32(d, x[3]);
            }
            function cmn(q, a, b, x, s, t) {
                a = add32(add32(a, q), add32(x, t));
                return add32((a << s) | (a >>> (32 - s)), b);
            }
            function ff(a, b, c, d, x, s, t) { return cmn((b & c) | ((~b) & d), a, b, x, s, t); }
            function gg(a, b, c, d, x, s, t) { return cmn((b & d) | (c & (~d)), a, b, x, s, t); }
            function hh(a, b, c, d, x, s, t) { return cmn(b ^ c ^ d, a, b, x, s, t); }
            function ii(a, b, c, d, x, s, t) { return cmn(c ^ (b | (~d)), a, b, x, s, t); }
            function md51(s) {
                const n = s.length;
                const state = [1732584193, -271733879, -1732584194, 271733878];
                let i;
                for (i = 64; i <= n; i += 64) { md5cycle(state, md5blk(s.substring(i - 64, i))); }
                s = s.substring(i - 64);
                const tail = Array(16).fill(0);
                for (i = 0; i < s.length; i++) tail[i >> 2] |= s.charCodeAt(i) << ((i % 4) << 3);
                tail[(i >> 2)] |= 0x80 << ((i % 4) << 3);
                if (i > 55) { md5cycle(state, tail); tail.fill(0); }
                tail[14] = n * 8; md5cycle(state, tail); return state;
            }
            function md5blk(s) {
                const blks = [];
                for (let i = 0; i < 64; i += 4) { blks[i >> 2] = s.charCodeAt(i) + (s.charCodeAt(i + 1) << 8) + (s.charCodeAt(i + 2) << 16) + (s.charCodeAt(i + 3) << 24); }
                return blks;
            }
            function rhex(n) {
                const s = "0123456789abcdef";
                let out = "";
                for (let j = 0; j < 4; j++) out += s[(n >> (j * 8 + 4)) & 0x0F] + s[(n >> (j * 8)) & 0x0F];
                return out;
            }
            function hex(x) { return x.map(rhex).join(""); }
            function add32(a, b) { return (a + b) & 0xFFFFFFFF; }
            return hex(md51(str));
        }

        _0x58fb1d(s) {
            let a = 0x15051505;
            let b = a;
            const length = s.length;
            let i = length - 1;
            while (i > 0) {
                a = (a ^ (s.charCodeAt(i) << ((length - i) % 30))) & 0x7fffffff;
                b = (b ^ (s.charCodeAt(i - 1) << (i % 30))) & 0x7fffffff;
                i -= 2;
            }
            return (a + b).toString(16).toLowerCase();
        }

        async _e(s) {
            s = String(s);
            const h = this.md5_hex(s);
            let result = h.substring(0, 3);
            let chunks, type_flag;
            if (/^\d+$/.test(s)) {
                chunks = [];
                for (let i = 0; i < s.length; i += 9) { chunks.push(parseInt(s.substring(i, i + 9)).toString(16)); }
                type_flag = "3";
            } else {
                chunks = [ Array.from(s).map(c => c.charCodeAt(0).toString(16)).join("") ];
                type_flag = "4";
            }
            result += type_flag + "2" + h.slice(-2);
            chunks.forEach((chunk, idx) => {
                let lenHex = chunk.length.toString(16);
                if (lenHex.length === 1) lenHex = "0" + lenHex;
                result += lenHex + chunk;
                if (idx < chunks.length - 1) result += "g";
            });
            if (result.length < 20) { result += h.slice(0, 20 - result.length); }
            result += this.md5_hex(result).slice(0, 3);
            return result;
        }

        async get_request_param() {
            let bid = await this._e(this.book_id)
            let cid = await this._e(this.chapter_id)
            const book = { b: bid, c: cid, ct: `${Math.floor(Date.now() / 1000)}`, pc: this.pc, prevChapter: "false", ps: this.ps, r: String(Math.floor(10000 * Math.random()) ** 2), sc: 0, st: 0, };
            const s = Object.entries(book).map(([k, v]) => `${k}=${v}`).join("&");
            book.s = this._0x58fb1d(s);
            return book;
        }
    }

    var bookInfo = {}
    let params = window.__book_params || {};
    var readProgress = null
    var contents = {}
    var clickedChapters = new Set();

    const OriginalXHR = window.XMLHttpRequest;
    const originalOpen = OriginalXHR.prototype.open;
    const originalSend = OriginalXHR.prototype.send;
    const targetPattern = '/web/book/chapter/';

    OriginalXHR.prototype.open = function (method, url, async, user, password) {
        this._url = url;
        return originalOpen.apply(this, arguments);
    };

    OriginalXHR.prototype.send = function (body) {
        if (this._url && this._url.includes(targetPattern)) {
            try { 
                let parsed = JSON.parse(body); 
                if (parsed.pc && parsed.ps) params = parsed;
            } catch(e){}
        } else if(this._url && this._url.includes('/web/book/getProgress')) {
            this.addEventListener('load', function () {
                try{ readProgress = JSON.parse(this.responseText); }catch(e) {}
            });
        }
        return originalSend.apply(this, arguments);
    };

    const originalFetch = window.fetch;
    window.fetch = async function() {
        const url = arguments[0];
        const options = arguments[1];
        if (url && typeof url === 'string' && url.includes(targetPattern)) {
            if (options && options.body) {
                try {
                    let parsed = JSON.parse(options.body);
                    if (parsed.pc && parsed.ps) params = parsed;
                } catch(e) {}
            }
        }
        return originalFetch.apply(this, arguments);
    };

    function htmlToMarkdown(html, options = {}) {
        if (typeof TurndownService === 'undefined') return html;
        const turndownService = new TurndownService({ headingStyle: 'atx', hr: '---', bulletListMarker: '-', codeBlockStyle: 'fenced' });
        try { return turndownService.turndown(html); } catch (error) { return html; }
    }

    function get_content(texts, type = 'e') {
        if (texts.length === 4) { texts.splice(2, 1); } else if (texts.length === 2) { type = 't' }
        let t = texts.map(s => s.slice(32)).join(""); t = t.slice(1);
        function a(s) {
            const length = s.length; if (length < 4) return [];
            const n = Math.min(4, Math.ceil(length / 10)); let tmp = "";
            for (let i = length - 1; i >= length - n; i--) { tmp += parseInt(s.charCodeAt(i).toString(2), 4).toString(); }
            const arr = []; const m = length - n - 2; const step = String(m).length; let i = 0;
            while (arr.length < 10 && i + step < tmp.length) {
                arr.push(parseInt(tmp.slice(i, i + step)) % m); arr.push(parseInt(tmp.slice(i + 1, i + 1 + step)) % m); i += step;
            }
            return arr;
        }
        function b(s, arr) {
            const chars = s.split("");
            for (let i = arr.length - 1; i >= 0; i -= 2) {
                for (let k of [1, 0]) {
                    const idx1 = arr[i] + k; const idx2 = arr[i - 1] + k;
                    const tmp = chars[idx1]; chars[idx1] = chars[idx2]; chars[idx2] = tmp;
                }
            }
            return chars.join("");
        }
        const b64 = b(t, a(t)).replace(/-/g, "+").replace(/_/g, "/").replace(/[^A-Za-z0-9+/]/g, "");
        let decodedText = atob(b64);
        const pattern = /[\xC0-\xDF][\x80-\xBF]|[\xE0-\xEF][\x80-\xBF]{2}|[\xF0-\xF7][\x80-\xBF]{3}/g;
        decodedText = decodedText.replace(pattern, (chunk) => {
            const l = chunk.length; const c = chunk;
            if (l === 4) {
                let val = ((c.charCodeAt(0) & 0x07) << 18) | ((c.charCodeAt(1) & 0x3F) << 12) | ((c.charCodeAt(2) & 0x3F) << 6) | (c.charCodeAt(3) & 0x3F) - 0x10000;
                return String.fromCharCode(0xD800 + (val >> 10), 0xDC00 + (val & 0x3FF));
            } else if (l === 3) { return String.fromCharCode(((c.charCodeAt(0) & 0x0F) << 12) | ((c.charCodeAt(1) & 0x3F) << 6) | (c.charCodeAt(2) & 0x3F)); }
            else { return String.fromCharCode(((c.charCodeAt(0) & 0x1F) << 6) | (c.charCodeAt(1) & 0x3F)); }
        });
        return decodedText;
    }

    async function getEpubContent(bookId, chapterId, pc, ps) {
        const wg = new WereadGenerateBrowser(bookId, chapterId, pc, ps || '11');
        const params_data = await wg.get_request_param();
        const bookType = bookInfo.book ? bookInfo.book.format : "epub";
        let urls = bookType === "epub" ? ["/web/book/chapter/e_0", "/web/book/chapter/e_1", "/web/book/chapter/e_3"] : ["/web/book/chapter/t_0", "/web/book/chapter/t_1"];
        const texts = [];
        for (let url of urls) {
            const data = await fetch(url, { "headers": { "content-type": "application/json;charset=UTF-8" }, "body": JSON.stringify(params_data), "method": "POST", "credentials": "include" }).then(resp => resp.text());
            texts.push(data);
        }
        return texts;
    }

    async function getBookInfo(bookId) {
        let data = await fetch('/web/book/publicchapterInfos', { "headers": { "content-type": "application/json;charset=UTF-8" }, "body": JSON.stringify({"bookIds": [bookId]}), "method": "POST", "credentials": "include" }).then(resp => resp.json());
        if (data.data[0].updated.length === 0) {
            data = await fetch('/web/book/chapterInfos', { "headers": { "content-type": "application/json;charset=UTF-8" }, "body": JSON.stringify({"bookIds": [bookId]}), "method": "POST", "credentials": "include" }).then(resp => resp.json());
        }
        return data;
    }

    window.__exporter_ready = true;
    window.__export_status = 'idle'; // 'idle', 'running', 'done', 'error'
    window.__export_progress = "";
    window.__export_result = null;
    window.__export_error = null;

    window.startExport = async function() {
        window.__export_status = 'running';
        window.__export_result = null;
        window.__export_error = null;
        window.__export_progress = "Initializing...";

        // Make sure to also check the window level in case it arrived late
        if (!params.pc || !params.ps) {
            if (window.__book_params && window.__book_params.pc) {
                params = window.__book_params;
            }
        }

        if (!params.pc || !params.ps) {
            window.__export_status = 'error';
            window.__export_error = "Keys not captured. Please flip a page manually.";
            return;
        }

        try {
            // --- Resolve bookId from multiple sources ---
            let bId = null;

            // Source 1: bookInfo already has book structure from API
            if (bookInfo && bookInfo.book && bookInfo.book.bookId) {
                bId = bookInfo.book.bookId;
            }
            // Source 2: bookInfo itself has bookId (direct API response item)
            else if (bookInfo && bookInfo.bookId) {
                bId = bookInfo.bookId;
            }
            // Source 3: Extract from current URL
            // URL format: /web/reader/<encoded_id>k<book_id>a<chapter_id>
            if (!bId) {
                const urlMatch = window.location.href.match(/web\/reader\/[^k]+k([^a]+)/);
                if (urlMatch) bId = urlMatch[1];
            }
            // Source 4: Try fetching from API using the ld+json @Id
            if (!bId) {
                const ldEl2 = document.querySelector('script[type="application/ld+json"]');
                if (ldEl2) {
                    try {
                        const parsed = JSON.parse(ldEl2.textContent);
                        const apiId = parsed['@Id'] || parsed['bookId'];
                        if (apiId) bId = apiId;
                    } catch(e) {}
                }
            }

            if (!bId) throw new Error('Could not determine book ID from any source.');

            window.__export_progress = `Fetching chapter list for book: ${bId}...`;
            
            // Fetch book chapter info
            const bookData = await getBookInfo(bId);
            if (!bookData || !bookData.data || !bookData.data[0]) {
                throw new Error('Failed to fetch book chapter info from API.');
            }
            const bookMeta = bookData.data[0];
            bookInfo = bookMeta; // Update global for future use

            const chapters = bookMeta.updated || [];
            if (chapters.length === 0) throw new Error('No chapters found for this book.');

            const title = (bookMeta.book && bookMeta.book.title) || bookMeta.title || 'Unknown Book';
            let fullMarkdown = `# ${title}\n\n`;
            
            for (let i = 0; i < chapters.length; i++) {
                const ch = chapters[i];
                window.__export_progress = `Exporting: ${ch.title} (${i + 1}/${chapters.length})`;
                try {
                    const texts = await getEpubContent(bId, ch.chapterUid, params.pc, params.ps);
                    fullMarkdown += `\n\n## ${ch.title}\n\n${htmlToMarkdown(get_content(texts))}`;
                } catch (e) {
                    fullMarkdown += `\n\n## ${ch.title}\n\n[Export Failed: ${e.message || e}]`;
                }
            }
            window.__export_result = fullMarkdown;
            window.__export_status = 'done';
            window.__export_progress = "Export completed.";
        } catch (e) {
            window.__export_status = 'error';
            window.__export_error = e.message || String(e);
            window.__export_progress = "Export failed.";
        }
    };

    window.getExportChunk = function(offset, length) {
        if (!window.__export_result) return null;
        let str = window.__export_result.substring(offset, offset + length);
        // 使用标准的 UTF-8 -> Base64 转换逻辑，处理多字节字符
        try {
            return btoa(unescape(encodeURIComponent(str)));
        } catch (e) {
            console.error("Base64 encoding failed:", e);
            return null;
        }
    };

    // Legacy support for older calls (optional, but keep for compatibility if needed)
    window.exportWholeBook = async function() {
        await window.startExport();
        if (window.__export_status === 'error') return "ERROR: " + window.__export_error;
        return window.__export_result;
    };

    const ldEl = document.querySelector('script[type="application/ld+json"]');
    if (ldEl) {
        try {
            bookInfo = JSON.parse(ldEl.textContent);
            if (bookInfo['@Id']) { getBookInfo(bookInfo['@Id']).then(info => { bookInfo = info.data[0]; }); }
        } catch (e) {}
    }
    window.__exporter_ready = true;
})();
