import os
import time
from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from WeReadScan import WeRead

def main():
    # 书籍 URL 列表 (在此填入你想下载的微信读书网页版URL)
    book_urls = [
        "https://weread.qq.com/web/reader/xxxxxx",
        # "https://weread.qq.com/web/reader/yyyyyy"
    ]

    print("="*50)
    print(f"微信读书批量爬虫 - 共 {len(book_urls)} 本待处理")
    print("="*50)

    # 配置 Edge 选项 (复用 start_scan.py 的配置)
    os.environ['http_proxy'] = ''
    os.environ['https_proxy'] = ''
    os.environ['no_proxy'] = '*'

    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('disable-infobars')
    options.add_argument('log-level=3')
    options.add_argument('--no-proxy-server')
    options.add_argument('--proxy-server="direct://"')
    options.add_argument('--proxy-bypass-list=*')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-extensions')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--disable-logging')
    
    user_data_dir = os.path.abspath(os.path.join(os.getcwd(), "edge_profile"))
    if not os.path.exists(user_data_dir):
        os.makedirs(user_data_dir)
    options.add_argument(f"user-data-dir={user_data_dir}")
    
    def create_driver():
        print("正在启动 Microsoft Edge 浏览器...")
        d = Edge(options=options)
        d.command_executor._client_config.timeout = 600
        d.set_page_load_timeout(150)
        d.set_script_timeout(600)
        return d

    driver = None
    try:
        driver = create_driver()
        with WeRead(driver, debug=True) as weread:
            print("正在检查登录状态...")
            weread.login() # 如果已登录会自动跳过，否则提示扫码
            
            for index, url in enumerate(book_urls, 1):
                print(f"\n[{index}/{len(book_urls)}] 正在处理: {url}")
                
                try:
                    # 尝试导出 Markdown
                    success = weread.export_markdown(url)
                    if success:
                        print(f"成功导出: {url}")
                    else:
                        print(f"导出失败: {url}")
                    
                    # 避免操作过快，休息 5 秒
                    if index < len(book_urls):
                        print("休息 5 秒后继续下一本...")
                        time.sleep(5)
                except Exception as e:
                    print(f"处理书籍时发生错误 ({url}): {e}")
                    # 如果发生严重错误（如浏览器崩溃），尝试重启浏览器
                    if "session" in str(e).lower() or "disconnected" in str(e).lower():
                        print("检测到浏览器连接断开，正在尝试重启...")
                        try: driver.quit()
                        except: pass
                        driver = create_driver()
                        weread.driver = driver
                        weread.login()
                    continue

    except KeyboardInterrupt:
        print("\n程序已被用户终止。")
    except Exception as e:
        print(f"\n发生严重错误: {e}")
    finally:
        if driver:
            try:
                driver.quit()
                print("浏览器已关闭。")
            except:
                pass

if __name__ == "__main__":
    main()
