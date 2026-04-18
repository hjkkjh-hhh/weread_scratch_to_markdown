'''
WeRead.py
Copyright 2020 by Algebra-FUN
ALL RIGHTS RESERVED.
'''

from matplotlib import pyplot as plt
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver

from .script import img2pdf, dir_check, os_start_file, clear_temp, escape
import os
import time
from time import sleep


class WeRead:
    """
        The agency who control `WeRead` web page with selenium webdriver to processing book scanning.

        `微信读书`网页代理，用于图书扫描

        :Args:
         - headless_driver:
                Webdriver instance with headless option set.
                设置了headless的Webdriver示例

        :Returns:
         - WeReadInstance

        :Usage:
            chrome_options = ChromeOptions()
            chrome_options.add_argument('--headless')

            headless_driver = Chrome(chrome_options=chrome_options)

            weread = WeRead(headless_driver)
    """

    def __init__(self, headless_driver: WebDriver, patience=30, debug=False):
        headless_driver.get('https://weread.qq.com/')
        headless_driver.implicitly_wait(5)
        self.driver: WebDriver = headless_driver
        self.patience = patience
        self.debug_mode = debug

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if not self.debug_mode:
            clear_temp('wrs-temp')

    def S(self, selector):
        return WebDriverWait(self.driver, self.patience).until(lambda driver: driver.find_element(By.CSS_SELECTOR, selector))

    def click(self, target):
        self.driver.execute_script('arguments[0].click();', target)

    def inject_exporter(self):
        """Inject local jQuery, Turndown and our custom exporter script"""
        print("Injecting exporter dependencies from local files...")
        
        base_dir = os.path.dirname(__file__)
        libs = [
            os.path.join(base_dir, 'jquery.min.js'),
            os.path.join(base_dir, 'turndown.js'),
            os.path.join(base_dir, 'exporter.js')
        ]
        # Intercept XHR and fetch before page loads using a lightweight script
        # since injecting jQuery/Turndown here would crash due to empty DOM.
        interceptor_code = """
        window.__book_params = {};
        const OriginalXHR = window.XMLHttpRequest;
        const originalOpen = OriginalXHR.prototype.open;
        const originalSend = OriginalXHR.prototype.send;
        OriginalXHR.prototype.open = function (method, url) {
            this._url = url;
            return originalOpen.apply(this, arguments);
        };
        OriginalXHR.prototype.send = function (body) {
            if (this._url && this._url.includes('/web/book/chapter/')) {
                try { 
                    let parsed = JSON.parse(body); 
                    if (parsed.pc && parsed.ps) window.__book_params = parsed;
                } catch(e){}
            }
            return originalSend.apply(this, arguments);
        };
        const originalFetch = window.fetch;
        window.fetch = async function() {
            const url = arguments[0];
            const options = arguments[1];
            if (url && typeof url === 'string' && url.includes('/web/book/chapter/')) {
                if (options && options.body) {
                    try {
                        let parsed = JSON.parse(options.body);
                        if (parsed.pc && parsed.ps) window.__book_params = parsed;
                    } catch(e) {}
                }
            }
            return originalFetch.apply(this, arguments);
        };
        """
        try:
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': interceptor_code
            })
            print("Successfully injected interceptor via CDP.")
        except Exception as e:
            print(f"CDP injection failed: {e}.")


    def export_markdown(self, book_url, save_at='.'):
        """
        Export the book contents directly to a Markdown file using JS decryption.
        """
        print(f'Starting text export for: {book_url}')
        
        # 增加脚本超时时间
        self.driver.set_script_timeout(1200)
        self.driver.set_page_load_timeout(150)
        
        # 注入轻量级拦截脚本（通过 CDP 确保在页面加载前注入，从而拦截初始 XHR）
        self.inject_exporter()

        self.driver.get(book_url)
        sleep(5) # 给初步加载和脚本执行一点时间
        
        # Now inject the heavy libraries
        base_dir = os.path.dirname(__file__)
        libs = [
            os.path.join(base_dir, 'jquery.min.js'),
            os.path.join(base_dir, 'turndown.js'),
            os.path.join(base_dir, 'exporter.js')
        ]
        combined_code = ""
        for lib_path in libs:
            if os.path.exists(lib_path):
                with open(lib_path, 'r', encoding='utf-8') as f:
                    combined_code += f.read() + "\n"
        self.driver.execute_script(combined_code)
        
        # WAIT for exporter to be ready here
        print("Waiting for exporter to be ready...")
        for _ in range(10):
            if self.driver.execute_script("return !!window.__exporter_ready && typeof window.exportWholeBook === 'function';"):
                print("Exporter ready.")
                break
            sleep(1)
        
        # 获取书名
        try:
            book_name = escape(self.S('.readerTopBar_title').text)
        except:
            book_name = "Unknown_Book_" + str(int(sleep(0) or 1))

        print(f"Exporting book: {book_name}")

        # 触发密钥抓取和导出流程
        max_retries = 5
        for retry in range(max_retries):
            print("Triggering export process...")
            self.driver.execute_script("window.startExport();")
            
            # 轮询状态
            done = False
            error = None
            last_progress = ""
            
            timeout_limit = 600 # 10分钟超时
            start_time = time.time()
            
            while time.time() - start_time < timeout_limit:
                try:
                    status = self.driver.execute_script("return window.__export_status;")
                    progress = self.driver.execute_script("return window.__export_progress;")
                    
                    if progress != last_progress:
                        print(f"  [Progress] {progress}")
                        last_progress = progress
                    
                    if status == 'done':
                        done = True
                        break
                    elif status == 'error':
                        error = self.driver.execute_script("return window.__export_error;")
                        break
                except Exception as e:
                    print(f"  [Wait] Polling error (might be page reload): {e}")

                sleep(1)
            
            if done:
                break
            
            if error and "Keys not captured" in error:
                if retry < max_retries - 1:
                    print(f"Wait! Keys not captured (Attempt {retry+1}/{max_retries}). Trying an auto-flip...")
                    try:
                        self.driver.execute_script("""
                            var rightBtn = document.querySelector('button.readerFooter_button, button.renderTarget_pager_button_right, button.readerTarget_pager_button_right, .readerFooter_button');
                            if (rightBtn) rightBtn.click();
                            else {
                                var evt = new KeyboardEvent('keydown', { 'keyCode': 39, 'which': 39, 'key': 'ArrowRight' });
                                document.dispatchEvent(evt);
                            }
                        """)
                    except: pass
                    sleep(3)
                    continue
                else:
                    print("\n" + "!"*50)
                    print("重要提示：自动翻页未能成功捕获解密密钥。")
                    print("请您在浏览器窗口中【手动点击右箭头翻一两页】，然后回到这里按【回车键】继续。")
                    print("!"*50 + "\n")
                    input("请在手动翻页后按回车...")
                    continue # Retry after manual flip
            elif error:
                print(f"Export Error: {error}")
                return False
            else:
                print("Export timed out.")
                return False

        try:
            # 获取最终结果 (分段提取，避免序列化失败)
            total_len = self.driver.execute_script("return window.__export_result ? window.__export_result.length : 0;")
            if total_len == 0:
                print("Final attempt failed: Result is empty or null.")
                return False
            
            chunk_size = 20000
            full_content = ""
            print(f"  [Retrieval] Total length: {total_len} chars. Fetching in chunks of {chunk_size} (Base64 Mode)...")
            
            for i in range(0, total_len, chunk_size):
                chunk_b64 = self.driver.execute_script(f"return window.getExportChunk({i}, {chunk_size});")
                if chunk_b64:
                    # 解码 Base64 并拼接到 full_content (处理 UTF-8)
                    try:
                        import base64
                        chunk_raw = base64.b64decode(chunk_b64).decode('utf-8')
                        full_content += chunk_raw
                    except Exception as e:
                        print(f"\n  [Retrieval] Warning: Chunk decoding failed at offset {i}: {e}")
                
                # 打印拉取进度
                percent = min(100, int((i + chunk_size) / total_len * 100))
                print(f"  [Retrieval] {percent}% ({min(i + chunk_size, total_len)}/{total_len})", end='\r')
                sleep(0.5)
            print("\n  [Retrieval] Done.")

            # 清理浏览器内存
            self.driver.execute_script("window.__export_result = null;")

            # 保存到本地
            save_path = os.path.join(save_at, f"{book_name}.md")
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(full_content)
            
            print(f"Success! Markdown saved to: {save_path}")
            os_start_file(save_path)
            return True
        except Exception as e:
            print(f"Export failed during file saving: {e}")
            return False

    def shot_full_canvas_context(self, file_name):
        try:
            renderTargetContainer = self.S('.renderTargetContainer')
            height = renderTargetContainer.get_property('offsetHeight') or 1000
            height += renderTargetContainer.get_property('offsetTop') or 0
            
            # 使用 innerWidth 避免 outerWidth 返回 0 的情况
            width = self.driver.execute_script("return window.innerWidth;") or 1000
            
            # 确保长宽有效
            width = max(int(width), 800)
            height = max(int(height), 800)
            
            self.driver.set_window_size(width, height + 100)
            sleep(1)
            
            content = self.S('.app_content')
            size = content.size
            if size['width'] > 0 and size['height'] > 0:
                content.screenshot(file_name)
            else:
                print("Warning: .app_content has 0 width/height, falling back to window screenshot.")
                self.driver.save_screenshot(file_name)
        except Exception as e:
            print(f"Warning: Failed to capture element screenshot ({e}), falling back to full window.")
            self.driver.save_screenshot(file_name)

    def check_all_image_loaded(self, frequency=10, max_wait_duration=30):
        """
        check if all image is loaded.

        检查图书Image是否全部加载完毕.
        """
        interval = 1/frequency

        try:
            img_unloaded = WebDriverWait(self.driver, 3).until(
                lambda driver: driver.find_elements(By.CSS_SELECTOR, 'img.wr_absolute'))
        except Exception:
            return False

        for _ in range(frequency*max_wait_duration):
            sleep(interval)
            for img in img_unloaded:
                if img.get_property('complete'):
                    img_unloaded.remove(img)
            if not len(img_unloaded):
                self.debug_mode and print('all image is loaded!')
                return True
        return False

    def login(self, wait_turns=15):
        """
        show QRCode to login weread.

        展示二维码以登陆微信读书

        :Args:
         - wait_turns: 
                Loop turns wait for scanning QRCode
                登陆二维码等待扫描的等待轮数

        :Usage:
            weread.login()
        """

        dir_check('wrs-temp')

        # 检查是否已经登录 (最高优先级：是否存在用户头像)
        print("Checking login status...")
        # 尝试查找已登录标志：头像、退出按钮、书架 URL 等
        is_logged_in = False
        try:
            # 常见的已登录标志选择器
            logged_in_selectors = [
                '.wr_index_page_top_section_header_user_avatar', 
                '.navBar_user_avatar', 
                '.wr_avatar',
                '.wr_index_page_top_section_header_user'
            ]
            for sel in logged_in_selectors:
                if self.driver.find_elements(By.CSS_SELECTOR, sel):
                    is_logged_in = True
                    print(f"Logged in detected via: {sel}")
                    break
            
            if not is_logged_in and ('web/shelf' in self.driver.current_url or 'web/reader' in self.driver.current_url):
                is_logged_in = True
                print('Logged in detected via URL.')
        except Exception:
            pass

        if is_logged_in:
            print('Success: Detected already logged in, skipping login flow.')
            return

        # 获取登录按钮
        login_btns = self.driver.find_elements(By.CSS_SELECTOR, '.wr_index_page_top_section_header_action_link, .navBar_link_Login')
        visible_login_btns = [btn for btn in login_btns if btn.is_displayed()]
        
        if not visible_login_btns:
            print('No visible login buttons found. We might already be logged in or page structure is different.')
            # 做个最后的双重检查：如果没有登录按钮，通常已经进去了
            return

        print(f'Found {len(visible_login_btns)} login button(s). Proceeding with QR code login...')
        # get QRCode for Login
        try:
            self.click(visible_login_btns[0])
            print('Login button clicked.')
        except Exception as e:
            print(f'Failed to click login button: {e}')
            return

        # 等待二维码出现
        print('Waiting for QR code to appear...')
        sleep(2) # 给一点渲染时间
        try:
            # 动态选择器查找
            qr_selectors = ['.wr_login_window_qrCode img', '.login_dialog_qrcode>img', 'img[src*="open.weixin.qq.com/connect/qrcode"]']
            qr_img = None
            for sel in qr_selectors:
                elements = self.driver.find_elements(By.CSS_SELECTOR, sel)
                if elements and elements[0].is_displayed():
                    qr_img = elements[0]
                    break
            
            if not qr_img:
                print("Could not find QR code element. Maybe login succeeded instantly?")
                return

            qr_img.screenshot('wrs-temp/login_qrcode.png')
            print('QR code screenshot saved to: wrs-temp/login_qrcode.png')
        except Exception as e:
            print(f'Detailed capture error: {e}')
            if not any(btn.is_displayed() for btn in self.driver.find_elements(By.CSS_SELECTOR, '.wr_index_page_top_section_header_action_link, .navBar_link_Login')):
                print('Login successful (Login buttons disappeared).')
                return
            raise e

        # 显示二维码
        try:
            login_qrcode = Image.open('wrs-temp/login_qrcode.png')
            plt.ion()
            plt.clf()
            plt.title('Scan this QRCode to Login.')
            plt.imshow(login_qrcode)
            plt.show()
            plt.pause(.001)
        except Exception as e:
            print(f'Warning: Display window error: {e}. Please manually scan wrs-temp/login_qrcode.png')

        # 等待扫码
        print(f'Waiting for you to scan the QR code. Max wait: {wait_turns}s...')
        for i in range(wait_turns):
            try:
                # 检查是否跳转或标志出现
                if any(sel for sel in ['.wr_avatar', '.navBar_user_avatar'] if self.driver.find_elements(By.CSS_SELECTOR, sel)):
                    print('Login Succeed!')
                    break
                if 'web/shelf' in self.driver.current_url or 'web/reader' in self.driver.current_url:
                    print('Login Succeed (URL redirected).')
                    break
            except Exception:
                pass
            plt.pause(1)
        else:
            print('Reach timeout, checking final status...')
            if any(btn.is_displayed() for btn in self.driver.find_elements(By.CSS_SELECTOR, '.wr_index_page_top_section_header_action_link, .navBar_link_Login')):
                raise Exception('WeRead.Timeout: Login timeout.')
            else:
                print('Login button gone, continuing anyway.')

        # close QRCode Window
        try:
            plt.ioff()
            plt.close()
        except:
            pass

    def dismiss_overlays(self):
        """Dismiss any active masks or overlays"""
        try:
            masks = self.driver.find_elements(By.CSS_SELECTOR, '.wr_mask_Show')
            for mask in masks:
                self.click(mask)
            sleep(1)
        except:
            pass

    def switch_to_context(self):
        """switch to main body of the book"""
        self.dismiss_overlays()
        sleep(1)
        try:
            # NEW: Using self.click (JS) to avoid intercepted error
            catalog_btn = self.S('button.readerControls_item.catalog')
            self.click(catalog_btn)
            sleep(2)
            # NEW: Find all potential chapter items
            chapter_btns = self.driver.find_elements(By.CSS_SELECTOR, '.readerCatalog_list_item, .readerCatalog_list li')
            if len(chapter_btns) > 1:
                # Typically the second item is the first real chapter
                self.click(chapter_btns[1])
            elif chapter_btns:
                self.click(chapter_btns[0])
        except Exception as e:
            print(f"Warning: Failed to switch context ({e}).")

    def set_font_size(self, font_size_index=1):
        """
        set font size
        """
        try:
            sleep(2)
            # 只有当面板没打开时才点击
            if not self.driver.find_elements(By.CSS_SELECTOR, '.vue-slider-mark'):
                btn = self.S('button.readerControls_item.fontSizeButton')
                self.click(btn)
                sleep(1)
            
            marks = self.driver.find_elements(By.CSS_SELECTOR, '.vue-slider-mark')
            if marks:
                # 尽量选择目标的索引，防止 nth-child 失效
                target_idx = min(len(marks)-1, font_size_index-1)
                self.click(marks[target_idx])
                print(f"Font size set to index {font_size_index}")
            
            # 点击内容区关闭设置面板
            content = self.S('.app_content')
            self.click(content)
        except Exception as e:
            print(f"Warning: Failed to set font size ({e}). Continuing...")

    def turn_light_on(self):
        try:
            sleep(1)
            # 找到白色主题按钮
            white_btn = self.driver.find_elements(By.CSS_SELECTOR, 'button.readerControls_item.white')
            if white_btn:
                self.click(white_btn[0])
                print("Light theme turned on.")
        except Exception as e:
            print(f"Warning: Failed to turn light on ({e}). Continuing...")
        sleep(1)

    def scan2pdf(self, book_url, save_at='.', binary_threshold=200, quality=100, show_output=True, font_size_index=1):
        """
        scan `weread` book to pdf and save offline.

        扫面`微信读书`的书籍转换为PDF并保存本地

        :Args:
         - book_url:
                the url of weread book which aimed to scan
                扫描目标书籍的ULR
         - save_at='.':
                the path of where to save
                保存地址
         - binary_threshold=200:
                threshold of scan binary
                二值化处理的阈值
         - quality=95:
                quality of scan pdf
                扫描PDF的质量
         - show_output=True:
                if show the output pdf file at the end of this method
                是否在该方法函数结束时展示生成的PDF文件
         - font_size_index=1:
                the index of font size(1-7)
                字体大小级别(1-7)
                In particular, 1 represents minimize, 7 represents maximize
                特别地，1为最小，7为最大

        :Usage:
            weread.scan2pdf('https://weread.qq.com/web/reader/a57325c05c8ed3a57224187kc81322c012c81e728d9d180')
        """
        print('Task launching...')

        # valid the url
        if 'https://weread.qq.com/web/reader/' not in book_url:
            raise Exception('WeRead.UrlError: Wrong url format.')

        # switch to target book url
        self.driver.get(book_url)
        print(f'navigate to {book_url}')
        sleep(5) # 等待页面初步加载

        # 尝试一些初始化设置，但不阻塞
        self.turn_light_on()
        self.set_font_size(font_size_index)
        self.dismiss_overlays()

        # switch to target book's cover
        print("Switching to book content...")
        self.switch_to_context()
        self.dismiss_overlays()

        # get the name of the book
        # NEW: .readerTopBar_title
        try:
            book_name = escape(self.S('.readerTopBar_title').text)
        except:
            book_name = "Unknown_Book_" + str(int(sleep(0) or 1)) # Fallback
        print(f'preparing to scan "{book_name}"')

        # check the dir for future save
        dir_check(f'wrs-temp/{book_name}/context')

        # used to store png_name for pdf converting
        png_name_list = []

        page = 1

        while True:
            sleep(2) # 页面加载和渲染需要时间

            # get chapter
            try:
                # NEW: Using the new chapter title selector
                chapter_el = self.driver.find_elements(By.CSS_SELECTOR, '.reader_chapter_title, span.readerTopBar_title_chapter')
                if chapter_el:
                    chapter = escape(chapter_el[0].text)
                else:
                    # Fallback: Check if catalog has an active item
                    chapter = "Chapter_" + str(page)
            except Exception:
                chapter = "Chapter_" + str(page)
            
            print(f'scanning chapter "{chapter}" (Page {page})')

            # locate the renderTargetContent
            try:
                context = self.S('.app_content, .renderTargetContainer')
            except:
                break

            # check all image loaded
            self.check_all_image_loaded()

            # context_scan2png
            png_name = f'wrs-temp/{book_name}/context/{chapter}_{page}'
            self.shot_full_canvas_context(f'{png_name}.png')

            png_name_list.append(png_name)
            print(f'save chapter scan {png_name}')

            # find next page or chapter button
            try:
                print("Looking for next button...")
                # 仅查找新版的翻页按钮，最多等 5 秒避免长时间卡死
                readerFooter = WebDriverWait(self.driver, 5).until(
                    lambda driver: driver.find_element(By.CSS_SELECTOR, 'button.renderTarget_pager_button_right')
                )
            except Exception:
                print("Could not find the next page button. Assuming end of book.")
                break

            readerFooterClass = readerFooter.get_attribute('class') or ''
            
            # 点击按钮前的检查
            if 'disabled' in readerFooterClass or readerFooter.get_attribute('disabled'):
                print("Next button disabled, ending scan.")
                break

            try:
                next_btn_text = readerFooter.text.strip()
            except:
                next_btn_text = ""

            if next_btn_text in ["下一章", "Next Chapter"]:
                print("go to next chapter")
                page = 1
            else:
                print(f"go to next page")
                page += 1

            # 使用 JavaScript点击按钮
            self.click(readerFooter)

        print('pdf converting...')

        # convert to pdf and save offline
        img2pdf(f'{save_at}/{book_name}', png_name_list,
                binary_threshold=binary_threshold, quality=quality)
        print('scanning finished.')
        if show_output:
            os_start_file(f'{save_at}/{book_name}.pdf')
