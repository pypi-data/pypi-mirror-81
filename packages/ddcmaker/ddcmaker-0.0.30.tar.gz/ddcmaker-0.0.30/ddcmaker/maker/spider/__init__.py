from ddcmaker.maker.spider.actions import normal
from ddcmaker.maker.spider.spider import Spider
from ddcmaker.maker.spider.actions.ai import AI_FEATURES


def init():
    normal_spider = Spider()
    normal_spider.run_action(normal.init_body)
