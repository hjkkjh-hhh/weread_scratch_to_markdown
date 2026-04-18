# 微信读书离线导出工具 (WeReadScan)

本项目是一个专门用于将“微信读书”网页版中的已购/免费图书离线导出为**高质量 Markdown**格式的爬虫自动化库。
利用基于 Selenium / Edge 的浏览器自动化技术，它能在一次扫码登录后，自动进行“翻页”操作拦截数据源接口，解密提取包括文本、层级标题、图片在内的电子书排版数据。

## ✨ 特性

- 🚀 **全新 API 拦截机制**：通过 CDP 注入脚本进行底层抓包拦截，无需再慢慢等待图片截图，直接导出原文！
- 📝 **高质量 Markdown 格式输出**：导出的内容使用严谨的 Markdown 语法组织章节标题和正文段落。
- 📦 **支持批量下载**：提供 `batch_scan.py`，配置好书本 URL 列表，坐下喝杯咖啡即可自动挂机处理完毕！
- 🧠 **自动化反爬策略绕过**：已配置完整的反爬选项与等待重试逻辑。
- 🧰 **免重复登录**：本地自动缓存 Edge `userData`，第一次扫码后之后均自动登录。

## 🛠️ 环境配置

环境配置非常简单，只需安装 Python 及 Edge 浏览器。

```shell
# 1. 克隆项目
git clone https://github.com/YourUsername/WeReadScan.git
cd WeReadScan

# 2. 创建并激活虚拟环境 (推荐)
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt
```

> **注意：**
> 1. 本项目依赖系统的 **Microsoft Edge** 浏览器，请确保你的电脑上已经安装它。
> 2. 请确保你的网络畅通（推荐直接连接，不要使用复杂的系统代理，必要时脚本会自动设置代理直连）。

## 📖 快速上手

### 模式一：单书交互模式 
适合只下载一本特定图书。全程带有交互提示，极易上手！

```shell
python start_scan.py
```
**步骤：**
1. 运行后，程序会自动启动 Edge 浏览器并打开微信读书官网。
2. 请在弹出的浏览器窗口中**使用微信扫码登录**（如果之前登录过，会自动跳过这一步）。
3. 回到终端，按照提示输入你要下载的书籍 URL（比如：`https://weread.qq.com/web/reader/xxxxxx`），按回车。
4. 程序将自动进行后台提取。导出成功后，会在当前目录下生成以**书名命名的 Markdown 文件**！

### 模式二：批量挂机模式
适合有多本书籍需要导出的场景。

1. 打开 `batch_scan.py` 脚本，找到顶部的 `book_urls` 列表。
2. 将你要下载的所有书籍所在的网页 URL 放入列表中：
   ```python
   book_urls = [
       "https://weread.qq.com/web/reader/xxxxxx",
       "https://weread.qq.com/web/reader/yyyyyy",
       # ...
   ]
   ```
3. 运行脚本：
   ```shell
   python batch_scan.py
   ```
4. 随后脚本会自动登录并依次为你导出所有所选书籍。

## 🔧 附加工具 (Markdown 整理)

如果你遇到了需要调整 `html/xml` 标签的情况，本项目还附属了一个后处理脚本 `convert_to_md.py`：

1. 把刚才导出的 Markdown 文件放入到项目根目录新建的 `input_md` 文件夹内。
2. 执行 `python convert_to_md.py`。
3. 清理完善过排版的 Markdown 将会输出在 `output_md` 文件夹中。

## ⚠️ 免责声明 (Disclaimer)

1. 本脚本仅限用于**已购/免费**图书的网页端抓取，方便个人自研、做学习笔记之用。**禁止用于商业利益、盗版资源制作和任何违法违规用途**！
2. 尊重腾讯微信读书及原版权方的合法权益。如果使用者使用本该脚本用于不当目的，将一切责任后果由使用者独自承担。
3. 任何使用本脚本产生的纠纷和争议，开发者概不负责。
