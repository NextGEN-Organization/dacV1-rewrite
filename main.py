import undetected_chromedriver as uc
from selenium_stealth import stealth
import time
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import random
import time


def browser():
# uc.TARGET_VERSION = 78
    options = uc.ChromeOptions()
    ua = UserAgent()
    userAgent = ua.chrome
    #print(userAgent)
    options.add_argument(f'user-agent={userAgent}')
    options.add_argument("--headless")
    #options.add_argument("--proxy-server=socks5://" + str(proxy))
    options.add_argument("--host-resolver-rules=\"MAP * ~NOTFOUND , EXCLUDE myproxy\"")
    #options.add_extension("./extensions/buster_chrome.crx")
    #options.add_extension("./extensions/xpather.crx")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--enable-features=ReaderMode")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')


    prefs1 = {"profile.managed_default_content_settings.images": 1,
        "profile.managed_default_content_settings.popups": 2,
        "profile.default_content_setting_values.notifications": 2,
        "profile.managed_default_content_settings.geolocation": 2,
        "profile.managed_default_content_settings.stylesheets": 2, }

    options.add_experimental_option("prefs", prefs1)

    options.binary_location = r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe"

    driver = uc.Chrome(chrome_options=options)

    stealth(driver,
        languages=["en-US", "en"],
        user_agent=userAgent,
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

    url = "https://discord.com/register"
    #url = "https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=en&ec=65620&flowName=GlifWebSignIn&flowEntry=ServiceLogin"
    driver.get(url)
    sleeptime = 0.6
    
    email = "testing1234crazytown{}@gmail.com".format(random.randint(0, 1000))
    username = "soaringhigh{}".format(random.randint(0, 1000))
    password = "birdhigh1234sky"
    selection_month = random.choice(['December', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September','October', 'November'])
    selection_day = random.randint(1, 28)

    try:
        wait = WebDriverWait(driver, 30)

        enter_searchbar = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        slow_typing(enter_searchbar, email, 30)
        time.sleep(sleeptime)

        enter_user = driver.find_element_by_name("username")
        slow_typing(enter_user, username, 30)
        time.sleep(sleeptime)


        enter_password = driver.find_element_by_name("password")
        slow_typing(enter_password, password, 30)
        time.sleep(sleeptime)

        enter_month = driver.find_element_by_id("react-select-2-input")
        enter_month.send_keys(selection_month, Keys.ENTER)
        time.sleep(sleeptime)

        enter_day = driver.find_element_by_id("react-select-3-input")
        enter_day.send_keys(selection_day, Keys.ENTER)
        time.sleep(sleeptime)

        enter_year = driver.find_element_by_id("react-select-4-input")
        slow_typing(enter_year, random.randint(1988, 1997), 30)
        enter_year.send_keys(Keys.ENTER)
        time.sleep(sleeptime)

        driver.save_screenshot("register.png")
        try:
            driver.find_element_by_xpath("//input[@type='checkbox']").click()
        except:
            pass
        driver.find_element_by_xpath("//button[@type='submit']").click()
    except Exception as e:
            print(e)

    time.sleep(10)
    driver.save_screenshot("check.png")
    print(gettoken(driver))
    driver.quit()


def gettoken(driver):
    headers = driver.execute_script(
        "var iframe = document.createElement('iframe'); " \
        "iframe.onload = function(){ " \
        "var ifrLocalStorage = iframe.contentWindow.localStorage; " \
        "console.log(ifrLocalStorage.getItem('fingerprint'));}; " \
        "iframe.src = 'about:blank'; " \
        "document.body.appendChild(iframe); " \
        "return iframe.contentWindow.localStorage.getItem('token') ")

    headers = headers.splitlines()
    token = str(headers).lstrip("['\"").rstrip("\"']")
    return token


def slow_typing(element, string, timeout):
    for i in str(string):
        sleepTime = random.randint(timeout-25, timeout+25)/1000
        element.send_keys(i)
        time.sleep(sleepTime)



browser()