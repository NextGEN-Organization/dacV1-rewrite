import asyncio
from classes.proxyops import ProxyChecker, ProxyScraper
from classes.baseoperations import BaseOperations
from pprint import pprint

from datetime import datetime
async def main():
    start = datetime.now()
    loop = asyncio.get_event_loop()
    ps = ProxyScraper("https")
    proxies = ps.auto_scrape()

    pc = ProxyChecker(proxyType="http", proxies=proxies)
    asyncio.run(pc.begin_checking())
    pc.proxy_cleaner()
    checked = pc.clean_dupe_origin_proxies()
    pc.write_to_file(checked, "config/proxies.txt")
    pprint(checked)
    print("Total seconds taken: {}".format(round((datetime.now() - start).total_seconds(), 2)))
    print("Checked {} proxies.".format(len(proxies)))
    print("There were {} usable proxies.".format(len(checked)))



if __name__ == "__main__":
    asyncio.run(main())
