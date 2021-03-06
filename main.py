import asyncio
from classes.proxyops import ProxyChecker, ProxyScraper
from classes.baseoperations import BaseOperations
from pprint import pprint

from datetime import datetime

async def auto_scrape_and_check():
    start = datetime.now()
    loop = asyncio.get_event_loop()
    ps = ProxyScraper("socks4")
    proxies = ps.auto_scrape()
    pc = ProxyChecker(proxyType="socks4", proxies=proxies) #always put http if using http/https proxies. It works for both.
    asyncio.run(pc.begin_checking())
    pc.proxy_cleaner()
    checked = pc.clean_dupe_origin_proxies()
    pc.write_to_file(checked, "config/proxies.txt")
    pprint(checked)
    print("The proxy checking took {} seconds.".format(round((datetime.now() - start).total_seconds(), 2)))
    print("Checked {} proxies.".format(len(proxies)))
    print("There were {} usable proxies.".format(len(checked)))

async def auto_check():
    start = datetime.now()
    loop = asyncio.get_event_loop()
    pc = ProxyChecker(proxyType="socks4") #always put http if using http/https proxies. It works for both.
    pc.load_proxies_from_file()
    proxies = pc.get_test_proxies()
    asyncio.run(pc.begin_checking())
    pc.proxy_cleaner()
    checked = pc.clean_dupe_origin_proxies()
    pc.write_to_file(checked, "config/proxies.txt")
    pprint(checked)
    print("The proxy checking took {} seconds.".format(round((datetime.now() - start).total_seconds(), 2)))
    print("Checked {} proxies.".format(len(proxies)))
    print("There were {} usable proxies.".format(len(checked)))



if __name__ == "__main__":
    # asyncio.run(auto_check())
    asyncio.run(auto_scrape_and_check())
