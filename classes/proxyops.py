import aiohttp
import asyncio
from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector
from .baseoperations import BaseOperations
from proxyscrape import create_collector
from concurrent.futures.thread import ThreadPoolExecutor

import nest_asyncio
nest_asyncio.apply()




class ProxyScraper():
    def __init__(self, proxyType):
        self.proxyType = proxyType

    def auto_scrape(self):
        collector = create_collector('my-collector', self.proxyType)
        uniqlines = set(("{}:{}".format(proxy[0], proxy[1]) for proxy in collector.get_proxies({'anonymous': True})))
        return uniqlines

    


class ProxyChecker():
    def __init__ (self, proxyType, proxies=[], timeout=5):
        self.proxyType = proxyType
        self.testProxies = proxies
        self.loop = asyncio.get_event_loop()
        self.proxyList = []
        self.del_proxylist = []
        self.timeout = aiohttp.ClientTimeout(total=timeout)



    async def begin_checking(self):
        tasks = (self.check_proxy(proxy, self.proxyType) for proxy in self.testProxies)
        self.loop.run_until_complete(asyncio.gather(*tasks))


    def load_proxies_from_file(self):
        self.testProxies = []
        with open("config/proxies.txt", "r") as fd:
            for line in fd.readlines():
                line = line.strip("\n")
                if not line:
                    continue
                self.testProxies.append(line)


    def proxy_cleaner(self):
        for proxy in self.proxyList:
            if proxy in self.del_proxylist:
                self.proxyList.remove(proxy)
        

    def get_test_proxies(self):
      return self.testProxies

    
    def get_proxies(self):
        return self.proxyList


    def clean_dupe_origin_proxies(self):
        domains = []
        cleanProxies = []
        for proxy in self.proxyList:
            domain = proxy.split('.')[0:2]
            if domain in domains:
                continue
            domains.append(domain)
            cleanProxies.append(proxy)
        return cleanProxies


    def write_to_file(self, list=None, filepath=None):
        if not list:
            list = self.proxyList
        if not filepath:
            filepath = "config/proxies.txt"
        with open(filepath, "w") as writeFile:
            [writeFile.write(proxy + "\n") for proxy in list]
        return


    async def check_proxy(self, proxy, proxyType):
        connector = ProxyConnector.from_url("{}://{}".format(proxyType, proxy))
        async with aiohttp.ClientSession(connector=connector, timeout=self.timeout) as session:
            responseJSON=""
            try:
                async with session.get('https://discord.com') as response:
                    while True:

                        try:
                            responseJSONpart = await response.read()
                        except asyncio.exceptions.IncompleteReadError as e:
                            responseJSON = responseJSON + e.partial.decode('utf-8')
                            continue
                            

                        responseJSON = responseJSON + responseJSONpart.decode('utf-8')
                        print(response.status)
                        self.proxyList.append(proxy)
                        break


            except Exception as e:
                result = BaseOperations.get_full_class_name(e)

                results = {
                    "python_socks._errors.ProxyConnectionError": lambda: print("Failed proxy connection: {}".format(proxy)),
                    "python_socks._errors.ProxyError": lambda: print("Proxy Error: {}".format(proxy)),
                    "asyncio.exceptions.TimeoutError": lambda: print("Proxy timed out. {}".format(proxy)),
                    "ssl.SSLCertVerificationError": lambda: print("SSLCertError: {}".format(proxy))
                }

                func = results.get(result, lambda: "Unknown error.")
                func()

                self.del_proxylist.append(proxy)






