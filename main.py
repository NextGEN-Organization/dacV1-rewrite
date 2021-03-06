import undetected_chromedriver as uc
from selenium_stealth import stealth
import time

options = uc.ChromeOptions()
options.add_argument("start-maximized")

# options.add_argument("--headless")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
#options.binary_path = r""
driver = uc.Chrome(chrome_options=options, executable_path=r"/home/generel/Documents/vscode_projects/python/dacV1-rewrite/chromedriver")

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

url = "https://bot.sannysoft.com/"
driver.get(url)
time.sleep(5)
driver.quit()