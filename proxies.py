import asyncio
from classes.proxyops import ProxyChecker, ProxyScraper
from classes.baseoperations import BaseOperations
from pprint import pprint
from datetime import datetime


async def auto_scrape_and_check():
    start = datetime.now()
    loop = asyncio.get_event_loop()

    ps = ProxyScraper("http")
    proxies = ps.proxyscrape_scrape()
    proxies = list(proxies) + ps.spys_proxy_scrape()

    pc = ProxyChecker(proxyType="http", proxies=proxies) #always put http if using http/https proxies. It works for both.
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

    pc = ProxyChecker(proxyType="http") #always put http if using http/https proxies. It works for both.
    pc.load_proxies_from_file("config/proxies.txt")

    cleaned = pc.clean_dupe_origin_proxies()
    proxies = pc.get_test_proxies()

    asyncio.run(pc.begin_checking())
    pc.proxy_cleaner()

    checked = pc.get_proxies()
    pc.write_to_file(checked, "config/proxies.txt")

    pprint(checked)
    print("The proxy checking took {} seconds.".format(round((datetime.now() - start).total_seconds(), 2)))
    print("Checked {} proxies.".format(len(proxies)))
    print("There were {} usable proxies.".format(len(checked)))


if __name__ == "__main__":
    #asyncio.run(auto_check())
    asyncio.run(auto_scrape_and_check())

