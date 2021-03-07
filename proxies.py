import asyncio
from classes.proxyops import ProxyChecker, ProxyScraper
from classes.baseoperations import BaseOperations
from pprint import pprint
from datetime import datetime


def auto_scrape_and_check():
    start = datetime.now()
    loop = asyncio.get_event_loop()

    ps = ProxyScraper("socks4")
    proxies = ps.proxyscrape_scrape()
    proxies = list(proxies) + ps.spys_proxy_scrape() + ps.proxyscan_io_scrape()
    pc = ProxyChecker(proxyType="socks4", proxies=proxies) #always put http if using http/https proxies. It works for both.
    loop.run_until_complete(pc.begin_checking())

    pc.proxy_cleaner()
    checked = pc.clean_dupe_origin_proxies()

    pc.write_to_file(checked, "config/proxies.txt")

    pprint(checked)
    print("The proxy checking took {} seconds.".format(round((datetime.now() - start).total_seconds(), 2)))
    print("Checked {} proxies.".format(len(proxies)))
    print("There were {} usable proxies.".format(len(checked)))
    return checked


def auto_check():
    start = datetime.now()
    loop = asyncio.get_event_loop()

    pc = ProxyChecker(proxyType="socks4", timeout=3) #always put http if using http/https proxies. It works for both.
    pc.load_proxies_from_file("config/proxies.txt")

    cleaned = pc.clean_dupe_origin_proxies()
    proxies = pc.get_test_proxies()

    loop.run_until_complete(pc.begin_checking())
    pc.proxy_cleaner()

    checked = pc.get_proxies()
    #pc.write_to_file(checked, "config/proxies.txt")

    pprint(checked)
    print("The proxy checking took {} seconds.".format(round((datetime.now() - start).total_seconds(), 2)))
    print("Checked {} proxies.".format(len(proxies)))
    print("There were {} usable proxies.".format(len(checked)))
    return checked


if __name__ == "__main__":
    auto_check()
    #asyncio.run(auto_scrape_and_check())

