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
from selenium.common.exceptions import WebDriverException
import random
import time
import proxies
import threading
from threading import Thread

proxyType = "socks4"
tokens = []
workers = 0


def await_tab(driver):
    global workers
    while True:
        try:
            WebDriverWait(driver, 10).until(lambda driver: driver.current_url == "https://discord.com/channels/@me")
            time.sleep(3)
            token = gettoken(driver)
            tokens.append(token)
            print("{}\n".format(token if token != None else "No token found."))
            driver.quit()
            break
        except:
            pass


def browser(proxy):
    global workers
    options = uc.ChromeOptions()
    ua = UserAgent()
    userAgent = ua.chrome
    #print(userAgent)
    options.add_argument(f'user-agent={userAgent}')
    options.add_argument("--headless")
    options.add_argument("--proxy-server={}://{}".format(proxyType, proxy))
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
    try:
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
        try:
            driver.get(url)
        except WebDriverException:
            workers -= 1
            driver.quit()
            return

        Thread(target=await_tab, args=(driver,), daemon=True).start()
        sleeptime = 0.4
        
        email = "testing1234crazytown{}@gmail.com".format(random.randint(0, 100000))
        username = "soaringhigh{}".format(random.randint(0, 100000))
        password = "birdhigh1234sky"
        selection_month = random.choice(['December', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September','October', 'November'])
        selection_day = random.randint(1, 28)

        try:
            wait = WebDriverWait(driver, 30)

            enter_searchbar = wait.until(EC.presence_of_element_located((By.NAME, "email")))
            slow_typing(enter_searchbar, email, 20)
            time.sleep(sleeptime)

            enter_user = driver.find_element_by_name("username")
            slow_typing(enter_user, username, 20)
            time.sleep(sleeptime)


            enter_password = driver.find_element_by_name("password")
            slow_typing(enter_password, password, 20)
            time.sleep(sleeptime)

            enter_month = driver.find_element_by_id("react-select-2-input")
            slow_typing(enter_month, selection_month, 20)
            enter_month.send_keys(Keys.ENTER)
            time.sleep(sleeptime)

            enter_day = driver.find_element_by_id("react-select-3-input")
            slow_typing(enter_day, selection_day, 20)
            enter_day.send_keys(Keys.ENTER)
            time.sleep(sleeptime)

            enter_year = driver.find_element_by_id("react-select-4-input")
            slow_typing(enter_year, random.randint(1988, 1997), 20)
            enter_year.send_keys(Keys.ENTER)
            time.sleep(sleeptime)


            try:
                driver.find_element_by_xpath("//input[@type='checkbox']").click()
            except Exception:
                pass
            driver.find_element_by_xpath("//button[@type='submit']").click()
            try:
                WebDriverWait(driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//iframe[contains(@title, "widget")]')))
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div#checkbox.checkbox"))).click()
                print("Found one!")
                # wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))).click()
            except Exception:
                print("failed to find iframe!")
                workers -=1
                driver.quit()
            #time.sleep(3)

            #driver.save_screenshot("images/register{}.png".format(workers))

        except Exception as e:
            print(e)
    except Exception as e:
        print(e)
    time.sleep(30)
    workers -=1
    driver.quit()
    return


def gettoken(driver):
    headers = driver.execute_script(
        "var iframe = document.createElement('iframe'); " \
        "iframe.onload = function(){ " \
        "var ifrLocalStorage = iframe.contentWindow.localStorage; " \
        "console.log(ifrLocalStorage.getItem('fingerprint'));}; " \
        "iframe.src = 'about:blank'; " \
        "document.body.appendChild(iframe); " \
        "return iframe.contentWindow.localStorage.getItem('token') ")
    try:
        headers = headers.splitlines()
        token = str(headers).lstrip("['\"").rstrip("\"']")
    except Exception as e:
        token = None
    return token


def slow_typing(element, string, timeout):
    for i in str(string):
        sleepTime = random.randint(timeout-15, timeout+15)/1000
        element.send_keys(i)
        time.sleep(sleepTime)



def write_to_output_file():
    global tokens
    while True:
        if (len(tokens) == 0):
            time.sleep(0.5)
            continue
        with open("config/tokens.txt", "a+") as results:
            [results.write(token + "\n") for token in tokens if token != None]
            tokens = []
        


def main():
    global workers
    proxyList = proxies.auto_scrape_and_check()
    print(threading.active_count())
    i = 0
    Thread(target=write_to_output_file, daemon=True).start()
    while True:
        while workers < 3:
            thread = Thread(target=browser, args=(proxyList[i],), daemon=True)
            thread.start()
            workers += 1
            i += 1
    time.sleep(100000)


if __name__ == "__main__":
    main()