import os
import sys
from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from WeReadScan import WeRead

def main():
    print("="*50)
    print("微信读书爬虫 (WeReadScan) - 启动器")
    print("="*50)

    # 0. 尝试绕过代理 (针对 TUN 模式或系统代理)
    os.environ['http_proxy'] = ''
    os.environ['https_proxy'] = ''
    os.environ['no_proxy'] = '*'

    # 1. 配置 Edge 选项
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('disable-infobars')
    options.add_argument('log-level=3')
    
    # 彻底禁用代理的多种尝试
    options.add_argument('--no-proxy-server')
    options.add_argument('--proxy-server="direct://"')
    options.add_argument('--proxy-bypass-list=*')
    
    # 稳定性增强
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-extensions')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--ssl-version-max=tls1.2')
    
    # 彻底关闭控制台日志输出
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--disable-logging')
    
    # 使用独立的配置文件目录
    user_data_dir = os.path.abspath(os.path.join(os.getcwd(), "edge_profile"))
    if not os.path.exists(user_data_dir):
        os.makedirs(user_data_dir)
    options.add_argument(f"user-data-dir={user_data_dir}")
    
    print("正在启动 Microsoft Edge 浏览器...")
    driver = None
    try:
        driver = Edge(options=options)
        # 设置页面加载超时
        driver.set_page_load_timeout(30)
    except Exception as e:
        print(f"启动浏览器失败: {e}")
        return

    try:
        # 在进入 WeRead 逻辑前先测试连接
        print("正在尝试连接微信读书官网...")
        try:
            driver.get('https://weread.qq.com/')
        except Exception as e:
            print(f"连接官网失败: {e}")
            print("这通常是由于网络环境（如 TUN 模式）导致的。请尝试关闭代理或在代理软件中将 weread.qq.com 设为直连。")
            return

        with WeRead(driver, debug=True) as weread:
            print("页面加载成功，请准备好微信扫码登录...")
            weread.login()
            
            print("\n" + "-"*50)
            book_url = input("请输入微信读书的书籍 URL (例如 https://weread.qq.com/web/reader/...): ").strip()
            
            if not book_url:
                print("未输入 URL，程序退出。")
                return

            print(f"开始处理书籍: {book_url}")
            
            # 1. 尝试新的文本导出模式 (Markdown)
            print("\n尝试直接导出 Markdown 文本 (推荐)...")
            success = weread.export_markdown(book_url)
            
            if success:
                print("\n" + "="*50)
                print("导出任务已完成！Markdown 文件已保存到当前目录。")
                print("=" * 50)
            else:
                # 2. 如果失败，询问是否使用旧版图片扫描
                print("\n" + "!"*50)
                print("Markdown 导出失败。是否尝试旧版的图片扫描模式？(生成图片 PDF, 耗时较长) (y/n)")
                choice = input().lower().strip()
                if choice == 'y':
                    print("启动旧版扫描模式...")
                    weread.scan2pdf(book_url)
                    print("\n" + "="*50)
                    print("扫描任务已尝试完成。")
                    print("=" * 50)
                else:
                    print("已取消旧版扫描。")

    except KeyboardInterrupt:
        print("\n程序已被用户终止。")
    except Exception as e:
        print(f"\n发生错误: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
