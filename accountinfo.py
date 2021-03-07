import requests
import time


def get_email(self):
    session = requests.Session()
    if(self.proxyMode != 0):
        proxee = self.proxyToUse
        proxy = self.buildProxyDict(self.proxyType, proxee)
        #session.proxies.update(proxy)

    headers = {
        'authority': 'www.yinsiduanxin.com',
        'method': 'POST',
        'path': '/api/email_apply',
        'accept-encoding': 'gzip, deflate, br',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.yinsiduanxin.com',
        'referer': 'https://www.yinsiduanxin.com/mail',
        'x-requested-with': 'XMLHttpRequest'
    }

    payload = {
        'site': '@mailscode.com'
    }

    response = session.post("https://www.yinsiduanxin.com/api/email_apply", headers=headers, data=payload, timeout=(3.05, 5))
    try:
        email = response.json()['data']
        return email
    except Exception:
        return False




def get_verification_code(email):
    headers = {
        'authority': 'www.yinsiduanxin.com',
        'method': 'POST',
        'path': '/api/email_get',
        'accept-encoding': 'gzip, deflate, br',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.yinsiduanxin.com',
        'referer': 'https://www.yinsiduanxin.com/mail',
        'x-requested-with': 'XMLHttpRequest'
    }
    payload = {
        'email': email  #urllib.parse.quote_plus(self.email)
    }

    while True:
        response = requests.post("https://www.yinsiduanxin.com/api/email_get", headers=headers, data=payload, timeout=(6.05, 12))
        if ("\"error_code\":0" in response.text):
            print("Received the verification email. Continuing.\n")
            link = (''.join(response.text.split('Verify Email: ')[1].split('\\n\\n')[0]).rstrip('\n\n')).replace('\\/', '/')
            break
        else:
            time.sleep(0.5)

    webpage = session.post(link, timeout=(6.05, 12))
    if(webpage.history):
        debug(str(webpage.status_code) + ", " + webpage.url)

        cheaders = {
            'authority': 'discord.com',
            'method': 'POST',
            'path': '/api/v8/auth/verify',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US',
            'authorization': token,
            'content-length': '145',
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/verify',
        }
        tokenToUse = ''.join(str(webpage.url).split('token=')[1])

        print("Checking for available captcha tokens.")
        i = 0
        while True:
            keyGet2 = requests.get('http://harvester.google.com:5000/api/token')
            if keyGet2.json()['success'] == False:
                if i == 0:
                    print("There are no available captchas right now. Please go solve one at the local address.\nThe code will pause until the captcha is solved.\n")
                    i += 1
                debug("could not get a second captcha key.")
                time.sleep(2)
                continue
            else:
                captchaKey2 = keyGet2.json()['results']
                print("Received a second captcha key. Continuing.\n")
                debug(captchaKey2)
                break

        cpayload = {
            'captcha_key': captchaKey2,
            'token': tokenToUse
        }


        del session.headers['accept-encoding']
        confirm = session.post('https://discord.com/api/v8/auth/verify', headers=cheaders, json=cpayload, timeout=(6.05, 12))
        #debug(str(confirm.request.headers))
        #for k in confirm.request.headers:
        #    print(k.lower())
        #debug(str(type(confirm.response.text)))
        print("Finished. Moving to next token.\n\n")
        debug(confirm.text)