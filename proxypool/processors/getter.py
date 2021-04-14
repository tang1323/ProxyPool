from loguru import logger
from proxypool.storages.redis import RedisClient
from proxypool.setting import PROXY_NUMBER_MAX
from proxypool.crawlers import __all__ as crawlers_cls


class Getter(object):
    """
    getter of proxypool
    """
    
    def __init__(self):
        """
        初始化数据库和爬虫程序
        """
        self.redis = RedisClient()
        self.crawlers_cls = crawlers_cls
        self.crawlers = [crawler_cls() for crawler_cls in self.crawlers_cls]
    
    def is_full(self):
        """
        如果代理池已满
        return: bool
        """
        return self.redis.count() >= PROXY_NUMBER_MAX
    
    @logger.catch
    def run(self):
        """
        运行爬虫获取代理
        :return:
        """
        if self.is_full():
            return
        for crawler in self.crawlers:
            logger.info(f'crawler {crawler} to get proxy')
            for proxy in crawler.crawl():
                self.redis.add(proxy)


if __name__ == '__main__':
    getter = Getter()
    getter.run()
